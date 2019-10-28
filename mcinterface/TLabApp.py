from .ValueRange import ValueRange
from .McSimRunner import McSimulationRunner
from .TFitApp import TFitAppQt

import numpy as np
import websockets
import json
import re
import asyncio

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLineEdit,  QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QFrame, QPushButton, QLabel, QInputDialog, QProgressDialog

from matplotlib.figure import Figure
from matplotlib import ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TLabAppQt(QWidget, McSimulationRunner):
    """"""
    def __init__(self, name, env_config, instr_params, gui=True, dummy=False, vr_name=''):
        QWidget.__init__(self, env_config=env_config, instr_params=instr_params)

        self.gui = gui
        self.dummy = dummy
        self.vr_name = vr_name
        self.progress_dialog = None
        self.timer = None
        self.time_passed = 0.
        self.steps_passed = 0
        self.log_scale_y = False
        self.sq_scale_x = False
        self.sim_status = '1/2 Подготовка'
        self.timer_p_int = self.configuration['Simulation poll timer']  # mcsec

        if not gui:
            return

        # setting up the figure and its canvas for plots
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.setFixedWidth(self.configuration['Plot Width'])
        self.canvas.setFixedHeight(self.configuration['Plot Height'])

        # setting up plot axes
        if ('1D detector file name' in self.configuration) and ('2D detector file name' in self.configuration):
            self.axes_1d_detector, self.axes_2d_detector = self.canvas.figure.subplots(nrows=1, ncols=2)
        elif '1D detector file name' in self.configuration:
            self.axes_1d_detector = self.canvas.figure.subplots()
            self.axes_2d_detector = None
        elif '2D detector file name' in self.configuration:
            self.axes_1d_detector = None
            self.axes_2d_detector = self.canvas.figure.subplots()
        self.figure.tight_layout()

        # adding plot scale button and registering click callback
        self.log_by = QPushButton('Лог. интенсивность')
        self.log_by.setFixedWidth(0.2 * self.configuration['Plot Width'])
        self.log_by.clicked.connect(self.on_btn_log_y)
        self.sq_bx = QPushButton('Кв. ось x')
        self.sq_bx.setFixedWidth(0.2 * self.configuration['Plot Width'])
        self.sq_bx.clicked.connect(self.on_btn_sq_x)

        # adding the button to run the fit app
        self.fit_b = QPushButton('Анализ результатов')
        self.fit_b.setFixedWidth(0.2 * self.configuration['Plot Width'])
        self.fit_b.clicked.connect(self.on_btn_fit)

        self.save_b = QPushButton('Сохранить результаты')
        self.save_b.setFixedWidth(0.2 * self.configuration['Plot Width'])
        self.save_b.clicked.connect(self.on_btn_save)

        # adding simulation parameters buttons and labels
        self.param_buttons, self.param_labels = [], []
        for i, param in enumerate(self.instr_params):
            self.param_buttons.append(QPushButton(param.gui_name))
            self.param_labels.append(QLabel(str(param)))
            self.param_labels[i].setFrameStyle(QFrame.Sunken | QFrame.Panel)
            self.param_buttons[i].clicked.connect(self.make_callback(i))

        # adding "Simulate" button and registering click callback
        self.run_b = QPushButton('Запуск эксперимента')
        self.run_b.clicked.connect(self.on_btn_run)

        # adding instrument scheme picture
        p_map = QPixmap(self.configuration['instrument scheme'])
        p_map = p_map.scaledToHeight(200, Qt.SmoothTransformation)
        scheme_label = QLabel()
        scheme_label.setPixmap(p_map)

        # setting up Qt window layout
        main_layout = QHBoxLayout()
        param_layout = QGridLayout()
        plot_layout = QVBoxLayout()
        tbr_layout = QHBoxLayout()
        log_layout = QVBoxLayout()
        u_plot_layout = QHBoxLayout()

        tbr_layout.addWidget(self.toolbar, 0)
        log_layout.addWidget(self.log_by, 0)
        log_layout.addWidget(self.sq_bx, 1)
        tbr_layout.addLayout(log_layout, 1)
        plot_layout.addLayout(tbr_layout, 0)
        plot_layout.addWidget(self.canvas, 1)
        u_plot_layout.addWidget(self.fit_b, 0, Qt.AlignRight)
        u_plot_layout.addWidget(self.save_b, 1, Qt.AlignLeft)
        plot_layout.addLayout(u_plot_layout, 3)
        plot_layout.addWidget(scheme_label, 4, Qt.AlignCenter)

        for i, param in enumerate(self.instr_params):
            param_layout.addWidget(self.param_buttons[i], i, 0)
            param_layout.addWidget(self.param_labels[i], i, 1)
        param_layout.addWidget(self.run_b, len(self.instr_params), 1)

        main_layout.addLayout(param_layout, 0)
        main_layout.addLayout(plot_layout, 1)

        self.setLayout(main_layout)

        self.setWindowTitle(name)

    def send_params(self, status='', params=True):
        msg = dict()
        msg['id'] = self.vr_name

        if status:
            msg['id'] += '_' + status

        if params:
            for param in self.instr_params:
                if type(param.dtype) == ValueRange:
                    msg[param.vr_name + 'start'] = param.value.start
                    msg[param.vr_name + 'end'] = param.value.end
                else:
                    msg[param.vr_name] = param.value

        msg = json.dumps(msg)

        async def send_data(data):
            async with websockets.connect(self.configuration['VR server uri']) as websocket:
                await websocket.send(data)
        try:
            asyncio.get_event_loop().run_until_complete(send_data(msg))
            print('Sent', self.configuration['VR server uri'], 'data', msg)
        except OSError as e:
            print(e)

    def make_callback(self, ii):
        if self.instr_params[ii].value_names:
            def callback():
                item, ok = QInputDialog.getItem(self, self.instr_params[ii].gui_name, self.instr_params[ii].gui_name,
                                                self.instr_params[ii].value_names,
                                                self.instr_params[ii].values.index(self.instr_params[ii].value), False)
                if ok:
                    self.instr_params[ii].update_by_name(item)
                    self.param_labels[ii].setText("%s" % str(self.instr_params[ii]))
                    self.send_params()
        elif self.instr_params[ii].dtype == int:
            def callback():
                res, ok = QInputDialog.getInt(self, self.instr_params[ii].gui_name, self.instr_params[ii].gui_name,
                                              self.instr_params[ii].value)
                if ok:
                    self.instr_params[ii].update(res)
                    self.param_labels[ii].setText("%s" % str(self.instr_params[ii]))
                    self.send_params()
        elif self.instr_params[ii].dtype == float:
            def callback():
                d, ok = QInputDialog.getDouble(self, self.instr_params[ii].gui_name, self.instr_params[ii].gui_name,
                                               self.instr_params[ii].value)
                if ok:
                    self.instr_params[ii].update(d)
                    self.param_labels[ii].setText("%s" % str(self.instr_params[ii]))
                    self.send_params()
        elif type(self.instr_params[ii].dtype) == ValueRange:
            def callback():
                text, ok = QInputDialog.getText(self, self.instr_params[ii].gui_name,
                                                self.instr_params[ii].gui_name, QLineEdit.Normal, str(self.instr_params[ii]))
                if ok and text != '':
                    self.instr_params[ii].update(text)
                    self.param_labels[ii].setText("%s" % str(self.instr_params[ii]))
                    self.send_params()
        else:
            def callback():
                pass

            print(self.instr_params[ii].dtype)
        return callback

    def _update_plot_axes(self):
        if self.axes_1d_detector:
            self.axes_1d_detector.clear()
            self.axes_1d_detector.set_title(self.result1d.title)
            self.axes_1d_detector.set_xlabel(self.result1d.xlabel)
            self.axes_1d_detector.set_ylabel(self.result1d.ylabel)
            if self.log_scale_y:
                self.axes_1d_detector.set_yscale('log', nonposy='mask')
            else:
                self.axes_1d_detector.set_yscale('linear')
            if self.sq_scale_x:
                self.axes_1d_detector.errorbar(np.sqrt(self.result1d.xdata), self.result1d.ydata, yerr=self.result1d.yerrdata,
                                               zorder=1)
                self.axes_1d_detector.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x ** 2)))
            else:
                self.axes_1d_detector.errorbar(self.result1d.xdata, self.result1d.ydata, yerr=self.result1d.yerrdata,
                                               zorder=1)
                self.axes_1d_detector.xaxis.set_major_formatter(
                    ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x)))
        if self.axes_2d_detector:
            self.axes_2d_detector.clear()
            self.axes_2d_detector.set_title(self.result2d.title)
            self.axes_2d_detector.set_xlabel(self.result2d.xlabel)
            self.axes_2d_detector.set_ylabel(self.result2d.ylabel)
            if self.log_scale_y:
                self.axes_2d_detector.imshow(np.log(self.result2d.data), extent=self.result2d.extent)
            else:
                self.axes_2d_detector.imshow(self.result2d.data, extent=self.result2d.extent)
        self.figure.tight_layout()
        self.canvas.draw()

    def on_timeout(self):
        status = self.sim_process.poll()

        if status is not None:
            self.progress_dialog.setValue(self.progress_dialog.maximum())
            print('Child process returned', status)
            return

        self.time_passed += 1E-3 * self.timer_p_int

        self.sim_stdout.flush()
        self.sim_stderr.flush()

        try:
            out_line = self.sim_stdout.readline().decode()
        except IOError:
            out_line = ''

        try:
            err_line = self.sim_stderr.readline().decode()
        except IOError:
            err_line = ''

        if out_line:
            print(out_line)
        if err_line:
            print(err_line)

        m = re.match(r'Trace ETA (?P<mes>[\d.]+) \[(?P<scale>min|s|h)\]', out_line)
        if m:
            self.time_passed = 0.
            if self.sim_status != '2/2 Вычисление':
                self.sim_status = '2/2 Вычисление'
                if m.group('scale') == 's':
                    self.sim_eta = float(m.group('mes'))
                elif m.group('scale') == 'min':
                    self.sim_eta = float(m.group('mes')) * 60.
                elif m.group('scale') == 'h':
                    self.sim_eta = float(m.group('mes')) * 3600.
            else:
                if m.group('scale') == 's':
                    self.sim_eta = max(self.sim_eta, float(m.group('mes')))
                elif m.group('scale') == 'min':
                    self.sim_eta = max(self.sim_eta, float(m.group('mes')) * 60.)
                elif m.group('scale') == 'h':
                    self.sim_eta = max(self.sim_eta, float(m.group('mes')) * 3600.)

        if (self.n_points == 1) or (self.sim_status == '1/2 Подготовка'):
            self.progress_dialog.setValue(int(100. * self.time_passed / self.sim_eta))
            self.progress_dialog.setLabelText(self.sim_status + ": %d сек" % (self.sim_eta - int(self.time_passed)))

        m = re.match(r'INFO: (?P<param>[\S.]+): (?P<val>[\d.]+)$', err_line)
        if m:
            self.sim_status = '2/2 Вычисление'
            self.steps_passed += 1
        if (self.n_points > 1) and (self.sim_status == '2/2 Вычисление'):
            self.progress_dialog.setValue(int(100. * self.steps_passed / self.n_points))
            self.progress_dialog.setLabelText(self.sim_status + ": %d / %d шагов" % (int(self.steps_passed), self.n_points))

    def await_simulation(self):
        if self.sim_process is None:
            return
        self.sim_eta = self.configuration['Compilation ETA']
        self.time_passed = 0.
        self.steps_passed = 0
        self.sim_status = '1/2 Подготовка'

        self.progress_dialog = QProgressDialog('Ход эксперимента', 'Стоп', 0, 100)
        self.progress_dialog.resize(300, self.progress_dialog.height())
        self.progress_dialog.canceled.connect(self.kill_simulation)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(self.timer_p_int)
        self.progress_dialog.exec()
        self.timer.stop()

        self.sim_process.wait()

    def on_btn_run(self, *args, **kwargs):
        self.send_params(status='experiment', params=True)

        if self.dummy:
            self.update_sim_results(self.configuration['Backup Data Directory'])
            self._update_plot_axes()
            self.send_params(status='experiment_end', params=False)
            return

        self.open_simulation(*args, **kwargs)
        self.await_simulation()

        if self.sim_process.poll() >= 0:
            self.update_sim_results()
            self._update_plot_axes()
            self._cleanup()
            self.send_params(status='experiment_end', params=False)
        else:
            self.send_params(status='experiment_cancel', params=False)

    def on_btn_log_y(self, *args):
        self.log_scale_y = not self.log_scale_y

        if self.log_scale_y:
            self.log_by.setText('Лин. интенсивность')
        else:
            self.log_by.setText('Лог. интенсивность')

        self._update_plot_axes()

    def on_btn_sq_x(self, *args):
        self.sq_scale_x = not self.sq_scale_x

        if self.sq_scale_x:
            self.sq_bx.setText('Лин. ось x')
        else:
            self.sq_bx.setText('Кв. ось x')

        self._update_plot_axes()

    def on_btn_fit(self, *args):
        if self.axes_1d_detector is not None and len(self.result1d.xdata) > 0:
            fit_app = TFitAppQt(self.result1d)
            fit_app.show()

    def on_btn_save(self, *args):
        options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print('Results saved to %s' % fileName)
            np.savetxt(fileName, np.stack((self.result1d.xdata, self.result1d.ydata, self.result1d.yerrdata)).T)
