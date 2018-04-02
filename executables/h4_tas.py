from mcinterface import GUIParameter, TLabAppQt, ValueRange
from instance import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Wavelength $\lambda$ [AA]', 'lambda', float, 2.4),
    GUIParameter('Scattering angle [deg.]', 'scat_angle', float, 10),
    GUIParameter('An angle [deg.]', 'an_angle', ValueRange(float), (40, 60)),
    GUIParameter('An angle steps', 'N_count', int, 100),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E6),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H4_TAS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h4_tas'),
    '1D detector file name': 'mccode.dat', '1D detector x': 'an_angle',
    '1D detector y': 'befanL_I', '1D detector yerr': 'befanL_ERR',
    'instrument scheme': os.path.join(config.img_path, 'h4_tas_scheme.tiff'),
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
    pinhole_sans_app = TLabAppQt(name='Triple Axis Spectrometer',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
