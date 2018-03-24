from mcinterface import GUIParameter, TLabApp
import platform
from instance import config
import os

"""
"""

instrument_params = (
    GUIParameter('Wavelength $\lambda$ [AA]', 'lambda', float, 1.727),
    GUIParameter('Sample #', 'sample_index', int, 0),
    GUIParameter('Neutron count [n]', 'n_count', int, 1E8),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H8_StressD.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h8_sd'),
    '1D detector file name': 'Detector.dat',
    'instrument scheme': os.path.join(config.img_path, 'h8_sd_scheme.tiff'),
    'Figure size X': ' 12', 'Figure size Y': ' 7'
}

if platform.system() == 'Darwin':
    app_config.update({
        'Mcrun executable path': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/bin',
        'Mcstas PYTHONHOME': '/Applications/McStas-2.4.app/Contents/Resources/mcstas/2.4/miniconda3',
        'MPI nodes': '8'
    })
elif platform.system() == 'Linux':
    app_config.update({
        'Mcrun executable path': '/usr/share/mcstas/2.4.1/bin',
        'MPI nodes': '4'
    })

if __name__ == '__main__':
    app = TLabApp(name='Stress Diffractometer',
                  env_config=app_config,
                  instr_params=instrument_params)
    app.run()
