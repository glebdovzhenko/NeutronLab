from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны селектора [\u212B]', 'lambda', float, 15),
    GUIParameter('Тип диафрагм', 'dia_type', int, 1, values=(0, 1),
                 value_names=('Квадратная', 'Круглая')),
    GUIParameter('Ширина диафрагмы 1 [мм]', 'slit1_w', int, 32),
    GUIParameter('Ширина диафрагмы 2 [мм]', 'slit2_w', int, 16),
    GUIParameter('Ширина диафрагмы 3 [мм]', 'slit3_w', int, 16),
    GUIParameter('Положение детектора', 'det_position', int, 3, values=(1, 2, 3),
                 value_names=('Ближнее', 'Среднее', 'Дальнее')),
    GUIParameter('Образец', 'sample_num', int, 1, values=(1, 2, 3, 4),
                 value_names=('#1', '#2', '#3', '#4')),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H1_SANS.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h1_SANS'),
    '2D detector file name': 'Detector2D.dat', '1D detector file name': 'QDetector.dat',
    '2D title': 'Позиционно-чувствительный детектор', '2D xlabel': 'положение x [м]', '2D ylabel': 'положение y [м]',
    '1D title': 'Результат интегрирования ПЧД', '1D xlabel': 'Переданный импульс q [1/\u212B]', '1D ylabel': 'Интенсивность [усл. ед.]',
    'instrument scheme': os.path.join(config.img_path, 'h1_sans.tiff'),
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
    print(sys.path)
    app = QApplication(sys.argv)
    pinhole_sans_app = TLabAppQt(name='H1 SANS',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())