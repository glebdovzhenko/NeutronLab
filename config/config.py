import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

instr_path = os.path.join(project_root, 'mcstas_data', 'instruments')
results_path = os.path.join(project_root, 'mcstas_data', 'results')
img_path = os.path.join(project_root, 'mcstas_data', 'images')