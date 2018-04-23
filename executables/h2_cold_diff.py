from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны источника [\u212B]', 'lambda', float, 3),
    GUIParameter('Расходимость коллиматора [угл. мин.]', 'div_col', float, 45),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H2_ColdDif.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h2_cnd'),
    '1D detector file name': 'detector.dat',
    '1D title': 'проверка 1', '1D xlabel': 'проверка 2', '1D ylabel': 'проверка 3',
    'instrument scheme': os.path.join(config.img_path, 'h2_cpd.tiff'),
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
    pinhole_sans_app = TLabAppQt(name='Cold Neutron Diffractometer',
                  env_config=app_config,
                  instr_params=instrument_params, dummy=True)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
