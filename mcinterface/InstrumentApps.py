import os

from .TLabApp import TLabAppQt
from .ValueRange import ValueRange
from .GuiParameter import GUIParameter
from .config import app_config, instr_path, results_path, img_path


class H1SansApp(TLabAppQt):
    def __init__(self, dummy=False):
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

        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H1_SANS.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h1_SANS'),
            '2D detector file name': 'Detector2D.dat', '1D detector file name': 'QDetector.dat',
            '2D title': 'Позиционно-чувствительный детектор', '2D xlabel': 'положение x [м]',
            '2D ylabel': 'положение y [м]',
            '1D title': 'Результат интегрирования ПЧД', '1D xlabel': 'Переданный импульс q [1/\u212B]',
            '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h1_sans.png'),
        })

        TLabAppQt.__init__(self, name='H1 SANS', env_config=config, instr_params=instrument_params, dummy=dummy)


class H2ColdApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 3),
            GUIParameter('Расходимость коллиматора [угл. мин.]', 'div_col', float, 45),
            GUIParameter('Образец', 'sample_num', int, 0, values=(0,),
                         value_names=('Na2Ca3Al2F14',)),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
        )

        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H2_ColdDif.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h2_cnd'),
            '1D detector file name': 'detector.dat',
            '1D title': 'Угловое распределение интенсивности',
            '1D xlabel': 'Угол рассеяния 2$\Theta$ [град]', '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h2_cpd.png'),
        })

        TLabAppQt.__init__(self, name='Cold Neutron Diffractometer', env_config=config,
                           instr_params=instrument_params, dummy=dummy)


class H3ReflApp(TLabAppQt):
    def __init__(self, dummy):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'monok_lambda', float, 5.2),
            GUIParameter('Угол рассеяния [град.]', 'scat_angle', ValueRange(float), (0.3, 2.5)),
            GUIParameter('Шаги угла рассеяния', 'N_count', int, 100),
            GUIParameter('Образец', 'sample_index', int, 0, values=(0, 1), value_names=('#1', '#2')),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E4),
        )
        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H3_RPN.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h3_rpn'),
            '1D detector file name': 'mccode.dat', '1D detector x': 'scat_angle', '1D detector y': 'Detector_I',
            '1D detector yerr': 'Detector_ERR',
            '1D title': 'Скан интенсивности отражения по углу рассеяния', '1D xlabel': 'Угол рассеяния [град]',
            '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h3_rpn.png'),
        })
        TLabAppQt.__init__(self, name='Reflectometer', env_config=config, instr_params=instrument_params, dummy=dummy)


class H4TasApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 2.4, vr_name='monohromwavelength'),
            GUIParameter('Угол рассеяния [град.]', 'scat_angle', float, 10, vr_name='dispersionangle'),
            GUIParameter('Угол анализатора [град.]', 'an_angle', ValueRange(float), (40, 60), vr_name='analizangle'),
            GUIParameter('Шаги по ан. углу', 'N_count', int, 100, vr_name='steps'),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E6, vr_name='neytronstatistic'),
        )

        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H4_TAS.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h4_tas'),
            '1D detector file name': 'mccode.dat', '1D detector x': 'an_angle',
            '1D detector y': 'befanL_I', '1D detector yerr': 'befanL_ERR',
            '1D title': 'Скан интенсивности отражения по углу анализатора',
            '1D xlabel': 'Угол анализатора [град]', '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h4_tas.png'),
        })

        TLabAppQt.__init__(self, name='Triple Axis Spectrometer', env_config=config,
                           instr_params=instrument_params, dummy=dummy, vr_name='atos')


class H5ThermApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 1.2),
            GUIParameter('Диаметр диафрагмы [мм]', 'dia_dia', int, 3, values=(3, 6, 10),
                         value_names=('3', '6', '10')),
            GUIParameter('Образец', 'sample_num', int, 1, values=(1, 2, 3, 4, 5),
                         value_names=('Cu', 'Si', 'Ge', 'Al2O3', 'Na2Ca3Al2F14')),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E9),
        )

        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H5_ThPD.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h5_tnd'),
            '1D detector file name': 'Detector1.th',
            '1D title': 'Угловое распределение интенсивности', '1D xlabel': 'Угол рассеяния 2$\Theta$ [град]',
            '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h5_thpd.png'),
        })

        TLabAppQt.__init__(self, name='Thermal Powder Diffractometer', env_config=config,
                           instr_params=instrument_params, dummy=dummy)


class H6DcdApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 2.2),
            GUIParameter('Угол качания [град.]', 'rock_angle', ValueRange(float), (0, 1)),
            GUIParameter('Шаги угла качания', 'N_count', int, 100),
            GUIParameter('Образец', 'is_sample', int, 1, values=(0, 1), value_names=('Да', 'Нет')),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E7),
        )
        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H6_DCD.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h6_dcd'),
            '1D detector file name': 'mccode.dat', '1D detector x': 'rock_angle', '1D detector y': 'Detector_I',
            '1D detector yerr': 'Detector_ERR',
            '1D title': 'Распределение интенсивности по углу качания',
            '1D xlabel': 'Угол качания [град.]', '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h6_dcd.png'),
        })

        TLabAppQt.__init__(self, name='Double Crystal Diffractometer',
                  env_config=config, instr_params=instrument_params, dummy=dummy)


class H7ScdApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 1.2),
            GUIParameter('Номер образца', 'sample_index', int, 1, values=(1, 2)),
            GUIParameter('Вращение образца вокруг x', 'rot_x', float, 90),
            GUIParameter('Вращение образца вокруг y', 'rot_y', float, 0),
            GUIParameter('Вращение образца вокруг z', 'rot_z', float, 0),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E8),
        )
        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H7_SD.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h7_scd'),
            '2D detector file name': 'psd.dat',
            '2D title': 'Позиционно чувствительный детектор', '2D xlabel': 'Угол рассеяния 2$\Theta_{x}$ [град]',
            '2D ylabel': 'Угол рассеяния 2$\Theta_{y}$ [град]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h7_scd.png'),
        })

        TLabAppQt.__init__(self, name='Single Crystal Diffractometer', env_config=config,
                  instr_params=instrument_params, dummy=dummy)


class H8StressApp(TLabAppQt):
    def __init__(self, dummy=False):
        instrument_params = (
            GUIParameter('Длина волны монохроматора [\u212B]', 'lambda', float, 1.727),
            GUIParameter('Нагрузка на образец', 'sample_index', int, 0, values=(0, 1, 2, 3, 4, 5, 6),
                         value_names=('0 МПа', '75 МПа', '145 МПа', '220 МПа', '290 МПа', '365 МПа', '440 МПа')),
            GUIParameter('Статистика нейтронов', 'n_count', int, 1E8),
        )
        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, 'H8_StressD.instr'),
            'Backup Data Directory': os.path.join(results_path, 'h8_sd'),
            '1D detector file name': 'Detector.dat',
            '1D title': 'Угловое распределение интенсивности', '1D xlabel': 'Угол рассеяния 2$\Theta$ [град]',
            '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, 'RU', 'h8_sd.png'),
        })

        TLabAppQt.__init__(self, name='Stress Diffractometer', env_config=config,
                           instr_params=instrument_params, dummy=dummy)


class PinholeSansApp(TLabAppQt):
    def __init__(self, dummy=False):
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

        config = app_config.copy()
        config.update({
            'Instr filename': os.path.join(instr_path, '00_pinhole_SANS.instr'),
            'Backup Data Directory': os.path.join(results_path, '00_pinhole_SANS'),
            '2D detector file name': 'PSDMonitor.dat', '1D detector file name': 'QDetector.dat',
            '2D title': 'Детектор', '2D xlabel': 'x [см]', '2D ylabel': 'y [см]',
            '1D title': 'I(q)', '1D xlabel': 'Волн. вектор q [1/\u212B]', '1D ylabel': 'Интенсивность [усл. ед.]',
            'instrument scheme': os.path.join(img_path, '00_pinhole_SANS.tiff'),
        })

        TLabAppQt.__init__(self, name='Pinhole SANS', env_config=config, instr_params=instrument_params, dummy=dummy)