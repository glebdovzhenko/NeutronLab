from mcinterface import GUIParameter, TLabAppQt
from instance import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Wavelength $\lambda$ [AA]', 'lambda', float, 15),
    GUIParameter('Slit 1 width [m]', 'slit1_w', float, 0.008),
    GUIParameter('Slit 2 width [m]', 'slit2_w', float, 0.008),
    GUIParameter('Slit 3 width [m]', 'slit3_w', float, 0.008),
    GUIParameter('Detector position', 'det_position', int, 3),
    GUIParameter('Sample #', 'sample_num', int, 1),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E8),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H1_SANS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h1_SANS'),
    '2D detector file name': 'Detector2D.dat', '1D detector file name': 'QDetector.dat',
    'instrument scheme': os.path.join(config.img_path, 'h1_sans_scheme.tiff'),
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
    pinhole_sans_app = TLabAppQt(name='H1 SANS',
                                 env_config=app_config,
                                 instr_params=instrument_params)
    pinhole_sans_app.show()
    sys.exit(app.exec_())

