import numpy as np
from scipy.signal import argrelextrema

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog

from lmfit.models import GaussianModel


class TFitAppQt(QDialog):
    """"""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.x_borders = [min(data.xdata), max(data.xdata)]

        self.log_scale = True
        self.accept_coordinates = False
        self.fit_model = GaussianModel()
        self.fit_params = None
        self.fit_result = None

        # setting up the figure and its canvas for plots
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.mpl_connect('button_press_event', self.on_mouse_click)
        self._update_plot_axes()

        # adding plot scale button and registering click callback
        self.log_b = QPushButton('Лин. интенсивность')
        self.log_b.clicked.connect(self.on_btn_log)

        # adding fit param labels and buttons
        self.xleft_b = QPushButton('Левая граница')
        self.xright_b = QPushButton('Правая граница')
        self.xleft_b.clicked.connect(self.set_xleft)
        self.xright_b.clicked.connect(self.set_xright)

        # adding fit result output label
        self.center_label = QLabel('-')

        plot_layout = QVBoxLayout()
        tbr_layout = QHBoxLayout()
        param_layout = QGridLayout()

        tbr_layout.addWidget(self.toolbar, 0)
        tbr_layout.addWidget(self.log_b, 1)
        param_layout.addWidget(self.xleft_b, 0, 0)
        param_layout.addWidget(self.xright_b, 0, 1)

        plot_layout.addLayout(tbr_layout, 0)
        plot_layout.addWidget(self.canvas, 1)
        plot_layout.addLayout(param_layout, 3)
        plot_layout.addWidget(self.center_label)

        self.setLayout(plot_layout)
        self.setWindowTitle('Анализ результатов')

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.accept_coordinates = True

    def set_xleft(self):
        d, ok = QInputDialog.getDouble(self, "Левая граница", "Значение:", self.x_borders[0],
                                       min(self.data.xdata), self.x_borders[1], 4)
        if ok:
            self.x_borders[0] = d
            dxs = self.data.xdata[(self.data.xdata >= self.x_borders[0]) & (self.data.xdata <= self.x_borders[1])]
            dys = self.data.ydata[(self.data.xdata >= self.x_borders[0]) & (self.data.xdata <= self.x_borders[1])]
            self.fit_result = dxs, self.fit_model.fit(dys, self.fit_params, x=dxs)
            self.update_interface()

    def set_xright(self):
        d, ok = QInputDialog.getDouble(self, "Правая граница", "Значение:", self.x_borders[1],
                                       self.x_borders[0], max(self.data.xdata), 4)
        if ok:
            self.x_borders[1] = d
            dxs = self.data.xdata[(self.data.xdata >= self.x_borders[0]) & (self.data.xdata <= self.x_borders[1])]
            dys = self.data.ydata[(self.data.xdata >= self.x_borders[0]) & (self.data.xdata <= self.x_borders[1])]
            self.fit_result = dxs, self.fit_model.fit(dys, self.fit_params, x=dxs)
            self.update_interface()

    def _update_plot_axes(self):
        self.axes.clear()
        self.axes.set_title(self.data.title)
        self.axes.set_xlabel(self.data.xlabel)
        self.axes.set_ylabel(self.data.ylabel)

        if self.log_scale:
            self.axes.set_yscale('log', nonposy='clip')
        else:
            self.axes.set_yscale('linear')

        self.axes.errorbar(self.data.xdata, self.data.ydata, yerr=self.data.yerrdata, zorder=1)
        if self.fit_result is not None:
            self.axes.plot(self.fit_result[0], self.fit_result[1].best_fit)
        self.canvas.draw()

    def on_btn_log(self, *args):
        self.log_scale = not self.log_scale

        if self.log_scale:
            self.log_b.setText('Лин. интенсивность')
        else:
            self.log_b.setText('Лог. интенсивность')
        self._update_plot_axes()

    def on_mouse_click(self, event):
        if not self.accept_coordinates:
            return
        if event.inaxes == self.axes:
            self.accept_coordinates = False

            coord_id = ((self.data.xdata - event.xdata) ** 2 + (self.data.ydata - event.ydata) ** 2).idxmin()
            id_mxs, = argrelextrema(np.array(self.data.ydata), np.greater)
            id_mis, = argrelextrema(np.array(self.data.ydata), np.less_equal)

            id_max = sorted(id_mxs, key=lambda x: abs(x - coord_id))[0]
            lb = sorted(id_mis, key=lambda x: (id_max - x) if x <= id_max else 10000)[0]
            rb = sorted(id_mis, key=lambda x: (x - id_max) if x >= id_max else 10000)[0]

            dxs = np.array(self.data.xdata[lb:rb])
            dys = np.array(self.data.ydata[lb:rb])
            self.x_borders = [self.data.xdata[lb], self.data.xdata[rb]]

            self.fit_params = self.fit_model.guess(self.data.ydata, self.data.xdata)
            self.fit_params['center'].set(event.xdata)
            self.fit_params['amplitude'].set(event.ydata)
            self.fit_params['sigma'].set(0.5 * (dxs[-1] - dxs[0]))

            self.fit_result = dxs, self.fit_model.fit(dys, self.fit_params, x=dxs)
            self.update_interface()

    def update_interface(self):
        self.xleft_b.setText('Левая граница: %f' % self.x_borders[0])
        self.xright_b.setText('Правая граница: %f' % self.x_borders[1])
        self.center_label.setText(
            'Центр: %0.6f +- %0.6f' % (
            self.fit_result[1].params['center'].value, self.fit_result[1].params['center'].stderr))
        self._update_plot_axes()


