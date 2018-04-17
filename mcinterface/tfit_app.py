import numpy as np

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog


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
        self.peak_c = 0.
        self.peak_w = 0.
        self.peak_a = 0.
        self.peak_x_min = 0.
        self.peak_x_max = 0.

        self.b_fit = QPushButton('Оптимизировать')

        layout = QVBoxLayout()

        # adding plot scale button and registering click callback
        self.log_scale = True
        self.log_b = QPushButton('Показать линейную интенсивность')
        self.log_b.clicked.connect(self.on_btn_log)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.log_b)

        l2 = QGridLayout()
        self.c_button = QPushButton('Центр')
        self.w_button = QPushButton('Ширина')
        self.a_button = QPushButton('Высота')
        self.x_min_button = QPushButton('Левая граница')
        self.x_max_button = QPushButton('Правая граница')
        self.c_label = QLabel('-')
        self.w_label = QLabel('-')
        self.a_label = QLabel('-')
        self.x_min_label = QLabel('-')
        self.x_max_label = QLabel('-')

        self.c_button.clicked.connect(self.set_c)
        self.w_button.clicked.connect(self.set_w)
        self.a_button.clicked.connect(self.set_a)
        self.x_min_button.clicked.connect(self.set_x_min)
        self.x_max_button.clicked.connect(self.set_x_max)

        l2.addWidget(self.c_button, 0, 0)
        l2.addWidget(self.w_button, 1, 0)
        l2.addWidget(self.a_button, 2, 0)
        l2.addWidget(self.x_min_button, 3, 0)
        l2.addWidget(self.x_max_button, 4, 0)
        l2.addWidget(self.c_label, 0, 1)
        l2.addWidget(self.w_label, 1, 1)
        l2.addWidget(self.a_label, 2, 1)
        l2.addWidget(self.x_min_label, 3, 1)
        l2.addWidget(self.x_max_label, 4, 1)
        layout.addLayout(l2)

        layout.addWidget(self.b_fit)

        self.setLayout(layout)

        self.canvas.mpl_connect('button_press_event', self.on_mouse_mpl_event)
        self._update_plot_axes()
        self.setWindowTitle('Анализ кривой')

    def set_c(self):
        self.peak_c, ok = QInputDialog.getDouble(self, 'Центр пика', "Центр:", 37.56, -10000, 10000, 2)
        if ok:
            self.c_label.setText(str(self.peak_c))

    def set_w(self):
        self.peak_w, ok = QInputDialog.getDouble(self, 'Ширина пика', "Ширина:", 37.56, -10000, 10000, 2)
        if ok:
            self.w_label.setText(str(self.peak_w))

    def set_a(self):
        self.peak_a, ok = QInputDialog.getDouble(self, 'Высота пика', "Высота:", 37.56, -10000, 10000, 2)
        if ok:
            self.a_label.setText(str(self.peak_a))

    def set_x_min(self):
        self.peak_x_min, ok = QInputDialog.getDouble(self, 'Левая граница', "Значение:", 37.56, -10000, 10000, 2)
        if ok:
            self.x_min_label.setText(str(self.peak_x_min))

    def set_x_max(self):
        self.peak_x_max, ok = QInputDialog.getDouble(self, 'Правая граница', "Значение:", 37.56, -10000, 10000, 2)
        if ok:
            self.x_max_label.setText(str(self.peak_x_max))

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == 65:
                self.accept_coordinates = True
        else:
            event.ignore()

    @staticmethod
    def f(x, *args):
        return args[0] * np.exp(-0.5 * ((x - args[1]) / args[2]) ** 2)

    def on_mouse_mpl_event(self, event):
        if (event.inaxes == self.axes_1d_detector) and (event.button == 1) and self.accept_coordinates:
            self.peak_c = event.xdata
            self.peak_w = event.ydata
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