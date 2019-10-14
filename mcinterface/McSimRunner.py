from .ValueRange import ValueRange
from .McCodeParsers import McArray, McColumns

from collections import defaultdict
from subprocess import PIPE, Popen
import fcntl
import random
import string
import signal
import shutil
import time
import os


class McSimulationRunner:
    """"""
    def __init__(self, env_config, instr_params):
        self.configuration = defaultdict(lambda: None)
        self.configuration.update(env_config)
        self.instr_params = instr_params
        self.sim_process = None
        # TODO: replace with actual ending time or something
        self.sim_eta = None
        self.n_points = None
        self.sim_stderr, self.sim_stdout = None, None

        # initialising variables for storing plotted data
        # noinspection PyTypeChecker
        self.configuration['Simulation Data Directory'] = os.path.join(
            self.configuration['Simulation Data Directory'],
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        )

        if not os.path.exists(self.configuration['Instr filename']):
            raise FileNotFoundError('Вы не разблокировали приложение! Обратитесь к инструкции.')


        if '1D detector file name' in self.configuration:
            prms = dict(xcolumn=self.configuration['1D detector x'], ycolumn=self.configuration['1D detector y'],
                        yerrcolumn=self.configuration['1D detector yerr'])
            if '1D title' in self.configuration:
                prms['title'] = self.configuration['1D title']
            if '1D xlabel' in self.configuration:
                prms['xlabel'] = self.configuration['1D xlabel']
            if '1D ylabel' in self.configuration:
                prms['ylabel'] = self.configuration['1D ylabel']
            self.result1d = McColumns(**prms)
        else:
            self.result1d = None

        if '2D detector file name' in self.configuration:
            prms = dict()
            if '2D title' in self.configuration:
                prms['title'] = self.configuration['2D title']
            if '2D xlabel' in self.configuration:
                prms['xlabel'] = self.configuration['2D xlabel']
            if '2D ylabel' in self.configuration:
                prms['ylabel'] = self.configuration['2D ylabel']
            self.result2d = McArray(**prms)
        else:
            self.result2d = None

    def get_instr_param(self, sim_name):
        for p in self.instr_params:
            if p.sim_name == sim_name:
                return p
        else:
            raise ValueError('No parameter %s' % str(sim_name))

    def update_instr_param(self, sim_name, new_val):
        for p in self.instr_params:
            if p.sim_name == sim_name:
                p.update(new_val)
                return
        else:
            raise ValueError('No parameter %s' % str(sim_name))

    def update_sim_results(self, data_d=None):
        if not data_d:
            data_d = os.path.join(self.configuration['Simulation Data Directory'], 'sim')

        if self.result1d:
            self.result1d.clear()
            self.result1d.fill(os.path.join(data_d, self.configuration['1D detector file name']))
        if self.result2d:
            self.result2d.clear()
            self.result2d.fill(os.path.join(data_d, self.configuration['2D detector file name']))

    def open_simulation(self, *args, **kwargs):
        """"""
        model_params = [x for x in self.instr_params if ((x.sim_name != 'n_count') and (x.sim_name != 'N_count'))]
        exec_params = '-c --mpi=%d %s -d %s -n %d' % (self.configuration['MPI nodes'],
                                                      self.configuration['Instr filename'],
                                                      'sim',
                                                      int(self.get_instr_param('n_count')))

        if any(map(lambda x: isinstance(x.dtype, ValueRange), model_params)):
            self.n_points = int(self.get_instr_param('N_count'))
            exec_params += ' -N %d' % self.n_points
        else:
            self.n_points = 1

        for param in model_params:
            exec_params += ' ' + param.console_repr

        env = os.environ.copy()
        if 'Mcstas PYTHONHOME' in self.configuration:
            env['PYTHONHOME'] = self.configuration['Mcstas PYTHONHOME']

        os.mkdir(self.configuration['Simulation Data Directory'])

        self.sim_process = Popen([os.path.join(self.configuration['Mcrun executable path'], 'mcrun'), exec_params],
                                 env=env, cwd=self.configuration['Simulation Data Directory'],
                                 stdout=PIPE,
                                 stderr=PIPE,
                                 preexec_fn=os.setsid)
        print(os.path.join(self.configuration['Mcrun executable path'], 'mcrun'), exec_params)

        self.sim_stderr, self.sim_stdout = self.sim_process.stderr, self.sim_process.stdout
        fcntl.fcntl(self.sim_stdout, fcntl.F_SETFL, fcntl.fcntl(self.sim_stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
        fcntl.fcntl(self.sim_stderr, fcntl.F_SETFL, fcntl.fcntl(self.sim_stderr, fcntl.F_GETFL) | os.O_NONBLOCK)

    def await_simulation(self):
        if self.sim_process is None:
            return

        for i in range(self.sim_eta):
            print(self.sim_eta - i)
            status = self.sim_process.poll()
            if status is None:
                time.sleep(1)
            else:
                print('Child process returned', status)
                break
        else:
            self.sim_process.wait()

    def kill_simulation(self):
        if self.sim_process is not None:
            if self.sim_process.poll() is None:
                # TODO: processes don't really die
                os.killpg(os.getpgid(self.sim_process.pid), signal.SIGTERM)
        self._cleanup()

    def _cleanup(self):
        shutil.rmtree(self.configuration['Simulation Data Directory'], ignore_errors=True)

    def run(self):
        self.open_simulation()
        self.await_simulation()
        self.update_sim_results()
        self._cleanup()
