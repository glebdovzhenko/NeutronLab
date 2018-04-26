from mcinterface import GUIParameter, TLabAppQt
from PyQt5.QtWidgets import QApplication
from config import config
import platform
import sys
import os

"""  
"""

instrument_params = (
    GUIParameter('Wavelength [\u212B]', 'Lambda', float, 4.5),
    GUIParameter('Wavelength STD [\u212B]', 'DLambda', float, 0.1),
    GUIParameter('Source to 1st slit [m]', 'DistSrcPin1', float, 1),
    GUIParameter('Source to 2nd slit [m]', 'DistSrcPin2', float, 10),
    GUIParameter('2nd slit to sample [m]', 'DistPinSamp', float, 1),
    GUIParameter('Sample to detector [m]', 'DistSampDet', float, 10),
    GUIParameter('Detector radius [m]', 'DetRadius', float, 4),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E8),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, '00_pinhole_SANS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, '00_pinhole_SANS'),
    '2D detector file name': 'PSDMonitor.dat', '1D detector file name': 'QDetector.dat',
    '2D title': 'Детектор', '2D xlabel': 'x [см]', '2D ylabel': 'y [см]',
    '1D title': 'I(q)', '1D xlabel': 'Волн. вектор q [1/\u212B]', '1D ylabel': 'Интенсивность [усл. ед.]',
    'instrument scheme': os.path.join(config.img_path, '00_pinhole_SANS.tiff'),
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
    pinhole_sans_app = TLabAppQt(name='Pinhole SANS',
                                 env_config=app_config,
                                 instr_params=instrument_params,
                                 gui=True, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())

