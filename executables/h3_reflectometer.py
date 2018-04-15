from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны источника [\u212B]', 'monok_lambda', float, 5.2),
    GUIParameter('Угол рассеяния [град.]', 'scat_angle', float, 0),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H3_RPN.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h3_rpn'),
    '2D detector file name': 'Detector.xy',
    '2D title': 'проверка 4', '2D xlabel': 'проверка 5', '2D ylabel': 'проверка 6',
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
                                 instr_params=instrument_params)
    pinhole_sans_app.show()
    sys.exit(app.exec_())