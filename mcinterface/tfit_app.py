
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QProgressDialog


class TFitAppQt(QDialog):
    """"""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.accept_coordinates = False
        self.axes_1d_detector = self.figure.add_subplot(111)
        self.data1d = data

        self.b_fit = QPushButton('Оптимизировать')

        layout = QVBoxLayout()

        # adding plot scale button and registering click callback
        self.log_scale = True
        self.log_b = QPushButton('Показать линейную интенсивность')
        self.log_b.clicked.connect(self.on_btn_log)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.log_b)
        layout.addWidget(self.b_fit)
        self.setLayout(layout)

        self.canvas.mpl_connect('button_press_event', self.on_mouse_mpl_event)
        self._update_plot_axes()
        self.setWindowTitle('Анализ кривой')

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == 65:
                self.accept_coordinates = True
        else:
            event.ignore()

    def on_mouse_mpl_event(self, event):
        if (event.inaxes == self.axes_1d_detector) and (event.button == 1) and self.accept_coordinates:
            coordinates, tth, dtth = self.data1d.run_gaussian_fit((event.xdata, event.ydata))
            self._update_plot_axes()
            self.axes_1d_detector.plot(coordinates[0], coordinates[1], color='r', zorder=2)
            self.axes_1d_detector.text(event.xdata, event.ydata, 'Центр: %.3f +- %.3f' % (tth, dtth),
                                       backgroundcolor='w')
            self.figure.canvas.draw()
            self.accept_coordinates = False

    def _update_plot_axes(self):
        self.axes_1d_detector.clear()
        self.axes_1d_detector.set_title(self.data1d.title)
        self.axes_1d_detector.set_xlabel(self.data1d.xlabel)
        self.axes_1d_detector.set_ylabel(self.data1d.ylabel)
        if self.log_scale:
            self.axes_1d_detector.set_yscale('log', nonposy='clip')
        else:
            self.axes_1d_detector.set_yscale('linear')

        self.axes_1d_detector.errorbar(self.data1d.xdata, self.data1d.ydata, yerr=self.data1d.yerrdata,
                                       zorder=1)
        self.figure.tight_layout()
        self.figure.canvas.draw()

    def on_btn_log(self, *args):
        self.log_scale = not self.log_scale

        if self.log_scale:
            self.log_b.setText('Показать линейную интенсивность')
        else:
            self.log_b.setText('Показать логарифмическую интенсивность')

        self._update_plot_axes()