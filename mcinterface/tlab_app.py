from .value_range import ValueRange
from .mcsim_runner import McSimulationRunner

import numpy as np

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QProgressDialog

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TLabAppQt(QDialog, McSimulationRunner):
    """"""
    def __init__(self, name, env_config, instr_params, gui=True, dummy=False):
        QDialog.__init__(self, env_config=env_config, instr_params=instr_params)
        self.gui = gui
        self.dummy = dummy
        self.progress_dialog = None
        self.timer = None
        self.time_passed = 0

        if not gui:
            return

        layout = QHBoxLayout()
        l_left = QGridLayout()
        l_right = QVBoxLayout()

        # initialising mode of reacting to mouse events
        self.accept_coordinates = False

        # setting up the figures for plots
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.setFixedWidth(self.configuration['Plot Width'])

        l_right.addWidget(self.toolbar, 0)
        l_right.addWidget(self.canvas, 1)

        # TODO: implement
        # plotting the instrument scheme
        # self.figure.add_axes([0.05, 0.0, 0.9, 0.25]).imshow(Image.open(self.configuration['instrument scheme']))
        # plt.axis('off')

        # adding "Simulate" button and registering click callback
        self.sim_b = QPushButton('Запуск эксперимента')
        l_left.addWidget(self.sim_b, len(self.instr_params), 1)
        self.sim_b.clicked.connect(self.on_btn_run)

        # adding plot scale button and registering click callback
        self.log_scale = True
        self.log_b = QPushButton('Показать линейную интенсивность')
        l_right.addWidget(self.log_b, 2)
        self.log_b.clicked.connect(self.on_btn_log)

        # adding parameter text boxes and registering update callbacks
        self.param_buttons, self.param_labels = [], []
        self.setup_instr_params()

        for i, param in enumerate(self.instr_params):
            l_left.addWidget(self.param_buttons[i], i, 0)
            l_left.addWidget(self.param_labels[i], i, 1)

        self.axes_1d_detector = None
        self.axes_2d_detector = None

        # TODO: implement
        # self.figure.canvas.mpl_connect('button_press_event', self.on_mouse_event)
        # self.figure.canvas.mpl_connect('key_press_event', self.on_key_press_event)

        layout.addLayout(l_left, 0)
        layout.addLayout(l_right, 1)
        self.setLayout(layout)
        self.setWindowTitle(name)

    def setup_instr_params(self):
        for i, param in enumerate(self.instr_params):
            self.param_buttons.append(QPushButton(param.gui_name))
            self.param_labels.append(QLabel(str(param)))
            self.param_labels[-1].setFrameStyle(QFrame.Sunken | QFrame.Panel)
            self.param_buttons[-1].clicked.connect(self.make_callback(i))

    def make_callback(self, ii):
        def callback():
            if self.instr_params[ii].dtype == int:
                res, ok = QInputDialog.getInt(self, self.instr_params[ii].gui_name, self.instr_params[ii].gui_name,
                                              self.instr_params[ii].value)
                if ok:
                    self.instr_params[ii].update(res)
                    self.param_labels[ii].setText("%d" % res)
            elif self.instr_params[ii].dtype == float:
                d, ok = QInputDialog.getDouble(self, self.instr_params[ii].gui_name, self.instr_params[ii].gui_name,
                                               self.instr_params[ii].value)
                if ok:
                    self.instr_params[ii].update(d)
                    self.param_labels[ii].setText("%g" % d)
            elif self.instr_params[ii].dtype == ValueRange:
                text, ok = QInputDialog.getText(self, self, self.instr_params[ii].gui_name,
                                                self.instr_params[ii].gui_name, str(self.instr_params[ii]))
                if ok and text != '':
                    self.instr_params[ii].update(text)
                    self.param_labels[ii].setText(text)
            else:
                pass
        return callback

    def _create_plot_axes(self):
        if ('1D detector file name' in self.configuration) and ('2D detector file name' in self.configuration):
            self.axes_1d_detector = self.figure.add_subplot(121)
            self.axes_2d_detector = self.figure.add_subplot(122)
        elif '1D detector file name' in self.configuration:
            self.axes_1d_detector = self.figure.add_subplot(111)
        elif '2D detector file name' in self.configuration:
            self.axes_2d_detector = self.figure.add_subplot(111)

    def _update_plot_axes(self):
        if self.axes_1d_detector:
            self.axes_1d_detector.clear()
            self.axes_1d_detector.set_title(self.result1d.title)
            self.axes_1d_detector.set_xlabel(self.result1d.xlabel)
            self.axes_1d_detector.set_ylabel(self.result1d.ylabel)
            if self.log_scale:
                self.axes_1d_detector.set_yscale('log', nonposy='clip')
            else:
                self.axes_1d_detector.set_yscale('linear')

            self.axes_1d_detector.errorbar(self.result1d.xdata, self.result1d.ydata, yerr=self.result1d.yerrdata,
                                           zorder=1)

        if self.axes_2d_detector:
            self.axes_2d_detector.clear()
            self.axes_2d_detector.set_title(self.result2d.title)
            self.axes_2d_detector.set_xlabel(self.result2d.xlabel)
            self.axes_2d_detector.set_ylabel(self.result2d.ylabel)
            if self.log_scale:
                self.axes_2d_detector.imshow(np.log(self.result2d.data), extent=self.result2d.extent)
            else:
                self.axes_2d_detector.imshow(self.result2d.data, extent=self.result2d.extent)
        self.figure.tight_layout()
        self.figure.canvas.draw()

    def update_pb(self):
        status = self.sim_process.poll()
        if status is None:
            self.time_passed += 1
            self.progress_dialog.setValue(self.time_passed)
            self.progress_dialog.setLabelText("Симуляция: %d сек" % (self.sim_eta - self.time_passed))
        else:
            print('Child process returned', status)
            self.progress_dialog.setValue(self.sim_eta)

    def await_simulation(self):
        if self.sim_process is None:
            return

        self.progress_dialog = QProgressDialog('Симуляция', 'Стоп', 0, self.sim_eta)
        self.progress_dialog.canceled.connect(self.kill_simulation)
        self.time_passed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pb)
        self.timer.start(1000)
        self.progress_dialog.exec()
        self.timer.stop()

        self.sim_process.wait()

    def on_btn_run(self, *args, **kwargs):
        if self.dummy:
            self.update_sim_results(self.configuration['Backup Data Directory'])
            self._create_plot_axes()
            self._update_plot_axes()
            return

        self.open_simulation(*args, **kwargs)
        self.await_simulation()

        if self.sim_process.poll() >= 0:
            self.update_sim_results()
            self._create_plot_axes()
            self._update_plot_axes()
            self._cleanup()

    def on_btn_log(self, *args):
        self.log_scale = not self.log_scale

        if self.log_scale:
            self.log_b.setText('Показать линейную интенсивность')
        else:
            self.log_b.setText('Показать логарифмическую интенсивность')

        self._update_plot_axes()
