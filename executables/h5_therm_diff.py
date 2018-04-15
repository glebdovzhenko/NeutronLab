from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны источника [\u212B]', 'lambda', float, 1.5),
    GUIParameter('Коллиматор 1', 'col1', float, 10),
    GUIParameter('Коллиматор 2', 'col2', float, 20),
    GUIParameter('Коллиматор 3', 'col3', float, 10),
    GUIParameter('Мозаичность монохроматора [угл. мин.]', 'mon_mos', float, 40),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H5_ThPD.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h5_tnd'),
    '1D detector file name': 'Detector1.th',
    '1D title': 'проверка 1', '1D xlabel': 'проверка 2', '1D ylabel': 'проверка 3',
    'instrument scheme': os.path.join(config.img_path, 'h5_tnd_scheme.tiff'),
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
    pinhole_sans_app = TLabAppQt(name='Thermal Powder Diffractometer',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=True)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
