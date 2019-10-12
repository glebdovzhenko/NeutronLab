from mcinterface import GUIParameter, TLabAppQt
from config import config
import sys
from PyQt5.QtWidgets import QApplication
import platform
import os

"""
"""

instrument_params = (
    GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 1.2),
    GUIParameter('Диаметр диафрагмы [мм]', 'dia_dia', int, 3, values=(3, 6, 10),
                 value_names=('3', '6', '10')),
    GUIParameter('Образец', 'sample_num', int, 1, values=(1, 2, 3, 4, 5),
                 value_names=('Cu', 'Si', 'Ge', 'Al2O3', 'Na2Ca3Al2F14')),
    GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
)

app_config = {
    'Instr filename': os.path.join(config.instr_path, 'H5_ThPD.instr'),
    'Simulation Data Directory': config.results_path,
    'Backup Data Directory': os.path.join(config.results_path, 'h5_tnd'),
    '1D detector file name': 'Detector1.th',
    '1D title': 'Угловое распределение интенсивности', '1D xlabel': 'Угол рассеяния 2$\Theta$ [град]',
    '1D ylabel': 'Интенсивность [усл. ед.]',
    'instrument scheme': os.path.join(config.img_path, 'h5_tnd.tiff'),
    'Plot Width': 900, 'Plot Height': 400,
    'VR server uri': 'ws://185.104.249.66:6789/',
}

if platform.system() == 'Darwin':
    app_config.update({
        'Mcrun executable path': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/bin',
        'Mcstas PYTHONHOME': '/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/miniconda3',
        'MPI nodes': 8
    })
elif platform.system() == 'Linux':
    app_config.update({
        'Mcrun executable path': '/usr/share/mcstas/2.5/bin',
        'MPI nodes': 4
    })

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = TLabAppQt(name='Thermal Powder Diffractometer',
                                 env_config=app_config,
                                 instr_params=instrument_params, dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
