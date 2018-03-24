from mcinterface import ValueRange, McColumns, McArray
from matplotlib import pyplot as plt
from collections import defaultdict
from matplotlib.widgets import Button, TextBox
import numpy as np
from PIL import Image
import os
import subprocess
import shutil
import random
import string


class TLabApp:
    def __init__(self, name, env_config, instr_params, gui=True, dummy=False):
        # reading config file
        self.configuration = defaultdict(lambda: None)
        self.configuration.update(env_config)
        self.instr_params = instr_params
        self.gui = gui
        self.dummy = dummy

        # initialising variables for storing plotted data
        self.configuration['Simulation Data Directory'] = os.path.join(self.configuration['Simulation Data Directory'],
                                                                       ''.join(random.choices(string.ascii_uppercase +
                                                                                              string.digits, k=10)))
        self.result1d = McColumns(xcolumn=self.configuration['1D detector x'],
                                  ycolumn=self.configuration['1D detector y'],
                                  yerrcolumn=self.configuration['1D detector yerr'])
        self.result2d = McArray()

        if not gui:
            return

        # initialising mode of reacting to mouse events
        self.accept_coordinates = False

        # setting up GUI window
        self.figure = plt.figure(name, figsize=(int(self.configuration['Figure size X']),
                                                int(self.configuration['Figure size Y'])))

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

            self.axes_1d_detector.errorbar(self.result1d.xdata, self.result1d.ydata, yerr=self.result1d.yerrdata, zorder=1)

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

        exec_params = '-c --mpi=%s %s -d %s -n %d' % (self.configuration['MPI nodes'],
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

        subprocess.run([os.path.join(self.configuration['Mcrun executable path'], 'mcrun'), exec_params], env=env,
                       cwd=self.configuration['Simulation Data Directory'])

    def _cleanup(self):
        shutil.rmtree(self.configuration['Simulation Data Directory'], ignore_errors=True)

    def run(self):
        if self.gui:
            plt.show()
        else:
            self.simulate()
            self.update_sim_results()
        self._cleanup()