from mcinterface import GUIParameter, TLabAppQt, ValueRange
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны источника [\u212B]', 'monok_lambda', float, 5.2),
    GUIParameter('Угол рассеяния [град.]', 'scat_angle', ValueRange(float), (0.3, 2.5)),
    GUIParameter('Шаги угла рассеяния', 'N_count', int, 100),
    GUIParameter('Образец', 'sample_index', int, 0, values=(0, 1), value_names=('#1', '#2')),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E4),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H3_RPN.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h3_rpn'),
    '1D detector file name': 'mccode.dat', '1D detector x': 'scat_angle', '1D detector y': 'Detector_I',
    '1D detector yerr': 'Detector_ERR',
    '1D title': 'Скан интенсивности отражения по углу рассеяния', '1D xlabel': 'Угол рассеяния [град]',
    '1D ylabel': 'Интенсивность [усл. ед.]',
    'instrument scheme': os.path.join(config.img_path, 'h3_rpn.tiff'),
    'Plot Width': 900, 'Plot Height': 400,
}

if platform.system() == 'Darwin':
    app_config.update({
        'Mcrun executable path': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/bin',
        'Mcstas PYTHONHOME': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/miniconda3',
        'MPI nodes': 8
    })
elif platform.system() == 'Linux':
    app_config.update({
        'Mcrun executable path': '/usr/share/mcstas/2.4.1/bin',
        'MPI nodes': 4
    })

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = TLabAppQt(name='Reflectometer',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
