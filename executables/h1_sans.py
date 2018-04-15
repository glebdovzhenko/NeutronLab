from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны селектора [\u212B]', 'lambda', float, 15),
    GUIParameter('Ширина диафрагмы 1 [мм]', 'slit1_w', int, 32),
    GUIParameter('Ширина диафрагмы 2 [мм]', 'slit2_w', int, 16),
    GUIParameter('Ширина диафрагмы 3 [мм]', 'slit3_w', int, 16),
    GUIParameter('Положение детектора', 'det_position', int, 3),
    GUIParameter('Номер образца', 'sample_num', int, 1),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E8),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H1_SANS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h1_SANS'),
    '2D detector file name': 'Detector2D.dat', '1D detector file name': 'QDetector.dat',
    '2D title': 'проверка 4', '2D xlabel': 'проверка 5', '2D ylabel': 'проверка 6',
    '1D title': 'проверка 1', '1D xlabel': 'проверка 2', '1D ylabel': 'проверка 3',
    'instrument scheme': os.path.join(config.img_path, 'h1_sans_scheme.tiff'),
    'Plot Width': 900
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
    pinhole_sans_app = TLabAppQt(name='H1 SANS',
                                 env_config=app_config,
                                 instr_params=instrument_params)
    pinhole_sans_app.show()
    sys.exit(app.exec_())

