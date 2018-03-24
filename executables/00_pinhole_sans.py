from mcinterface import GUIParameter, TLabApp
from instance import config
import os

"""  
"""

instrument_params = (
    GUIParameter('Wavelength $\lambda$ [AA]', 'Lambda', float, 4.5),
    GUIParameter('Wavelength STD $\delta\lambda/\lambda$ [AA]', 'DLambda', float, 0.1),
    GUIParameter('Source to 1st slit [m]', 'DistSrcPin1', float, 1),
    GUIParameter('Source to 2nd slit [m]', 'DistSrcPin2', float, 10),
    GUIParameter('2nd slit to sample [m]', 'DistPinSamp', float, 1),
    GUIParameter('Sample to detector [m]', 'DistSampDet', float, 10),
    GUIParameter('Detector radius [m]', 'DetRadius', float, 4),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E7),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, '00_pinhole_SANS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, '00_pinhole_SANS'),
    '2D detector file name': 'PSDMonitor.dat', '1D detector file name': 'QDetector.dat',
    'Mcrun executable path': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/bin',
    'Mcstas PYTHONHOME': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/miniconda3',
    'instrument scheme': os.path.join(config.img_path, '00_pinhole_SANS.tiff'),
    'MPI nodes': '8', 'Figure size X': ' 12', 'Figure size Y': ' 7'
}


if __name__ == '__main__':
    app = TLabApp(name='Pinhole SANS',
                  env_config=app_config,
                  instr_params=instrument_params,
                  gui=True, dummy=False)
    app.run()
