from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Wavelength $\lambda$ [AA]', 'lambda', float, 1.2),
    GUIParameter('Sample #', 'sample_index', int, 1),
    GUIParameter('Sample rotation x', 'rot_x', float, 90),
    GUIParameter('Sample rotation y', 'rot_y', float, 0),
    GUIParameter('Sample rotation x', 'rot_z', float, 0),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E8),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H7_SD.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h7_scd'),
    '2D detector file name': 'psd.dat',
    'instrument scheme': os.path.join(config.img_path, 'h7_scd_scheme.tiff'),
    'Figure size X': 12, 'Figure size Y': 7
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
    pinhole_sans_app = TLabAppQt(name='Single Crystal Diffractometer',
                  env_config=app_config,
                  instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
