from mcinterface import GUIParameter, TLabAppQt, ValueRange
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 2.2),
    GUIParameter('Угол качания [град.]', 'rock_angle', ValueRange(float), (0, 1)),
    GUIParameter('Шаги угла качания', 'N_count', int, 100),
    GUIParameter('Образец', 'is_sample', int, 1, values=(0, 1), value_names=('Да', 'Нет')),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E7),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H6_DCD.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h6_dcd'),
    '1D detector file name': 'mccode.dat', '1D detector x': 'rock_angle', '1D detector y': 'Detector_I',
    '1D detector yerr': 'Detector_ERR',
    '1D title': 'Распределение интенсивности по углу качания',
    '1D xlabel': 'Угол качания [град.]', '1D ylabel': 'Интенсивность [усл. ед.]',
    'instrument scheme': os.path.join(config.img_path, 'h6_dcd.tiff'),
    'Plot Width': 900, 'Plot Height': 400,
    'VR server uri': 'ws://185.104.249.66:6789/',
}

if platform.system() == 'Darwin':
    app_config.update({
        'Mcrun executable path': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/bin',
        'Mcstas PYTHONHOME': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/miniconda3',
        'MPI nodes': 8
    })
elif platform.system() == 'Linux':
    app_config.update({
        'Mcrun executable path': '/usr/share/mcstas/2.5/bin',
        'MPI nodes': 4
    })

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = TLabAppQt(name='Double Crystal Diffractometer',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())