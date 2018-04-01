from .value_range import ValueRange
from .mccode_parsers import McArray, McColumns
from .mcsim_runner import McSimulationRunner

from matplotlib.widgets import Button, TextBox
from matplotlib import pyplot as plt
from collections import defaultdict
from subprocess import Popen, PIPE
from PIL import Image
import numpy as np
import shutil
import random
import string
import time
import os
import re

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QInputDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TLabApp:
    def __init__(self, name, env_config, instr_params, gui=True, dummy=False):
        # reading config file
        self.configuration = defaultdict(lambda: None)
        self.configuration.update(env_config)
        self.instr_params = instr_params
        self.gui = gui
        self.dummy = True

        # initialising variables for storing plotted data
        self.configuration['Simulation Data Directory'] = os.path.join(self.configuration['Simulation Data Directory'],
                                                                       ''.join(random.choices(string.ascii_uppercase +
                                                                                              string.digits, k=10)))
        self.result1d = McColumns(xcolumn=self.configuration['1D detector x'],
                                  ycolumn=self.configuration['1D detector y'],
                                  yerrcolumn=self.configuration['1D detector yerr'])
        self.result2d = McArray()
        self.update_sim_results()
        self.dummy = dummy

        if not gui:
            return

        # initialising mode of reacting to mouse events
        self.accept_coordinates = False

        # setting up GUI window
        self.figure = plt.figure(name, figsize=(self.configuration['Figure size X'],
                                                self.configuration['Figure size Y']))

        # plotting the instrument scheme
        self.figure.add_axes([0.05, 0.0, 0.9, 0.25]).imshow(Image.open(self.configuration['instrument scheme']))
        plt.axis('off')

        # adding "Simulate" button and registering click callback
        self.sim_b = Button(self.figure.add_axes([0.4, 0.3, 0.1, 0.04]), 'Simulate!')
        self.sim_b.on_clicked(self.on_btn_run)

        # adding plot scale button and registering click callback
        self.log_scale = True
        self.log_b = Button(self.figure.add_axes([0.64, 0.9, 0.1, 0.04]), 'Log Scale On')
        self.log_b.on_clicked(self.on_btn_log)

        # adding parameter text boxes and registering update callbacks
        self.text_boxes = []
        for i, param in enumerate(reversed(self.instr_params)):
            self.text_boxes.append(TextBox(self.figure.add_axes([0.17, 0.3 + 0.7 * i / len(self.instr_params),
                                                                 0.1, 0.04]), param.gui_name + '  ',
                                           initial=str(param.value)))
            self.text_boxes[-1].on_submit(param.update)

        self.axes_1d_detector = None
        self.axes_2d_detector = None

        self.figure.canvas.mpl_connect('button_press_event', self.on_mouse_event)
        self.figure.canvas.mpl_connect('key_press_event', self.on_key_press_event)

    def update_instr_param(self, sim_name, new_val):
        for p in self.instr_params:
            if p.sim_name == sim_name:
                p.update(new_val)
                return
        else:
            raise ValueError('No parameter %s' % str(sim_name))

    def on_btn_log(self, *args):
        self.log_scale = not self.log_scale

        if self.log_scale:
            self.log_b.label.set_text('Log Scale On')
        else:
            self.log_b.label.set_text('Log Scale Off')

        self._update_plot_axes()

    def _create_plot_axes(self):
        if '1D detector file name' in self.configuration:
            if '2D detector file name' in self.configuration:
                self.axes_1d_detector = self.figure.add_axes([0.36, 0.45, 0.3, 0.4])
                self.axes_2d_detector = self.figure.add_axes([0.65, 0.45, 0.4, 0.4])
            else:
                self.axes_1d_detector = self.figure.add_axes([0.36, 0.45, 0.6, 0.4])
        elif '2D detector file name' in self.configuration:
            self.axes_2d_detector = self.figure.add_axes([0.36, 0.45, 0.4, 0.4])

        if self.axes_2d_detector:
            self.axes_2d_detector.set_axis_off()

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
        self.figure.canvas.draw()

    def update_sim_results(self):
        if self.dummy:
            directory = self.configuration['Backup Data Directory']
            print('# Dummy mode, getting pre-simulated data...')
        else:
            directory = os.path.join(self.configuration['Simulation Data Directory'], 'sim')

        if '1D detector file name' in self.configuration:
            self.result1d.clear()
            self.result1d.fill(os.path.join(directory, self.configuration['1D detector file name']))
        if '2D detector file name' in self.configuration:
            self.result2d.clear()
            self.result2d.fill(os.path.join(directory, self.configuration['2D detector file name']))

    def on_btn_run(self, *args, **kwargs):
        if not self.dummy:
            self.simulate(*args, **kwargs)

        self.update_sim_results()
        self._create_plot_axes()
        self._update_plot_axes()

    def on_mouse_event(self, event):
        if (event.inaxes == self.axes_1d_detector) and (event.button == 1) and self.accept_coordinates:
            coordinates, tth, dtth = self.result1d.run_gaussian_fit((event.xdata, event.ydata))
            self._update_plot_axes()
            self.axes_1d_detector.plot(coordinates[0], coordinates[1], color='r', zorder=2)
            self.axes_1d_detector.text(event.xdata, event.ydata, '2$\Theta$ = %.3f +- %.3f' % (tth, dtth),
                                       backgroundcolor='w')
            self.figure.canvas.draw()
            self.accept_coordinates = not self.accept_coordinates

    def on_key_press_event(self, event):
        if event.key == 'a':
            self.accept_coordinates = not self.accept_coordinates

    def simulate(self, *args, **kwargs):
        """
        """
        p_count = [x for x in self.instr_params if x.sim_name == 'n_count']
        s_count = [x for x in self.instr_params if x.sim_name == 'N_count']
        model_params = [x for x in self.instr_params if ((x.sim_name != 'n_count') and (x.sim_name != 'N_count'))]

        exec_params = '-c --mpi=%d %s -d %s -n %d' % (self.configuration['MPI nodes'],
                                                      self.configuration['Instr filename'],
                                                      'sim',
                                                      int(*p_count))

        if any(map(lambda x: isinstance(x.dtype, ValueRange), model_params)):
            exec_params += ' -N %d' % int(*s_count)

        for param in model_params:
            exec_params += ' ' + param.console_repr

        env = os.environ.copy()
        if 'Mcstas PYTHONHOME' in self.configuration:
            env['PYTHONHOME'] = self.configuration['Mcstas PYTHONHOME']

        self._cleanup()
        os.mkdir(self.configuration['Simulation Data Directory'])
        print(env)
        print([os.path.join(self.configuration['Mcrun executable path'], 'mcrun'), exec_params])
        with Popen([os.path.join(self.configuration['Mcrun executable path'], 'mcrun'), exec_params], env=env,
                   cwd=self.configuration['Simulation Data Directory'], stdout=PIPE) as process:
            expr = re.compile(r'Trace ETA (?P<mes>[\d.]+) \[(?P<scale>min|s|h)\]')
            eta = []
            while True:
                line = process.stdout.readline()
                if not line and not process.poll():
                    break
                elif line:
                    line = line.decode()
                    print(line)
                    m = expr.match(line)
                    if m:
                        if m.group('scale') == 's':
                            eta.append(float(m.group('mes')))
                        elif m.group('scale') == 'min':
                            eta.append(float(m.group('mes')) * 60.)
                        elif m.group('scale') == 'h':
                            eta.append(float(m.group('mes')) * 3600.)
                    if len(eta) == self.configuration['MPI nodes'] - 1:
                        eta = np.mean(eta)
                        break
                else:
                    time.sleep(1)
            if not eta:
                eta = 0.
            print('# ETA %f sec' % eta)
            process.wait()

    def _cleanup(self):
        shutil.rmtree(self.configuration['Simulation Data Directory'], ignore_errors=True)

    def run(self):
        if self.gui:
            plt.show()
        else:
            if not self.dummy:
                self.simulate()
            self.update_sim_results()
        self._cleanup()


class TLabAppQt(QDialog, McSimulationRunner):
    """"""
    def __init__(self, name, env_config, instr_params, gui=True, dummy=False):
        QDialog.__init__(self, env_config=env_config, instr_params=instr_params)
        self.gui = gui
        self.dummy = dummy

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

        l_right.addWidget(self.toolbar, 0)
        l_right.addWidget(self.canvas, 1)

        # TODO: implement
        # plotting the instrument scheme
        # self.figure.add_axes([0.05, 0.0, 0.9, 0.25]).imshow(Image.open(self.configuration['instrument scheme']))
        # plt.axis('off')

        # adding "Simulate" button and registering click callback
        self.sim_b = QPushButton('Simulate!')
        l_left.addWidget(self.sim_b, len(self.instr_params), 1)
        self.sim_b.clicked.connect(self.on_btn_run)

        # adding plot scale button and registering click callback
        self.log_scale = True
        self.log_b = QPushButton('Log Scale On')
        l_right.addWidget(self.log_b, 2)
        self.log_b.clicked.connect(self.on_btn_log)

        # adding parameter text boxes and registering update callbacks
        self.param_requests, self.param_values = [], []
        for i, param in enumerate(self.instr_params):
            self.param_requests.append(QPushButton(param.gui_name))
            self.param_values.append(QLabel(str(param)))
            self.param_values[-1].setFrameStyle(QFrame.Sunken | QFrame.Panel)
            l_left.addWidget(self.param_requests[-1], i, 0)
            l_left.addWidget(self.param_values[-1], i, 1)
            # TODO: implement
            # self.text_boxes[-1].on_submit(param.update)

        self.axes_1d_detector = None
        self.axes_2d_detector = None

        # TODO: implement
        # self.figure.canvas.mpl_connect('button_press_event', self.on_mouse_event)
        # self.figure.canvas.mpl_connect('key_press_event', self.on_key_press_event)

        layout.addLayout(l_left, 0)
        layout.addLayout(l_right, 1)
        self.setLayout(layout)
        self.setWindowTitle(name)

    def _create_plot_axes(self):
        if self.axes_2d_detector:
            self.axes_2d_detector.set_axis_off()
        if '1D detector file name' in self.configuration:
            self.axes_1d_detector = self.figure.add_subplot(121)
        if '2D detector file name' in self.configuration:
            self.axes_2d_detector = self.figure.add_subplot(122)

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

    def on_btn_run(self, *args, **kwargs):
        if not self.dummy:
            self.open_simulation(*args, **kwargs)

        self.await_simulation()
        if not self.dummy:
            self.update_sim_results()
        else:
            self.update_sim_results(self.configuration['Backup Data Directory'])
        self._create_plot_axes()
        self._update_plot_axes()

    def on_btn_log(self, *args):
        self.log_scale = not self.log_scale

        if self.log_scale:
            self.log_b.setText('Log Scale On')
        else:
            self.log_b.setText('Log Scale Off')

        self._update_plot_axes()