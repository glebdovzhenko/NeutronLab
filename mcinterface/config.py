import os
import platform

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

instr_path = os.path.join(project_root, 'mcstas_data', 'instruments')
results_path = os.path.join(project_root, 'mcstas_data', 'results')
img_path = os.path.join(project_root, 'mcstas_data', 'images')

app_config = {
    'Simulation Data Directory': results_path,
    'Plot Width': 900, 'Plot Height': 400,
    'VR server uri': 'ws://185.104.249.66:6789/',
    'Simulation poll timer': 10,  # mcsec
    'Compilation ETA': 50
}

if platform.system() == 'Darwin':
    app_config.update({
        'Mcrun executable path': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/bin',
        'Mcstas PYTHONHOME': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/miniconda3',
        'MPI nodes': 8
    })
elif platform.system() == 'Linux':
    app_config.update({
        'Mcrun executable path': '/usr/share/mcstas/2.4.1/bin',
        'MPI nodes': 4
    })
