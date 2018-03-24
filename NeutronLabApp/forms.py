from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class SimplePlotForm(FlaskForm):
    xs = StringField('x range', default='0,1', validators=[DataRequired()])
    submit = SubmitField('Run')


class PinholeSANSForm(FlaskForm):
    wl = FloatField('Wavelength', default='4.5', validators=[DataRequired()])
    wl_std = FloatField('Wavelength STD', default='0.1', validators=[DataRequired()])
    d1 = FloatField('Source to 1st slit', default='1', validators=[DataRequired()])
    d2 = FloatField('Source to 2nd slit', default='10', validators=[DataRequired()])
    d3 = FloatField('2nd slit to sample', default='1', validators=[DataRequired()])
    d4 = FloatField('Sample to detector', default='10', validators=[DataRequired()])
    r = FloatField('Detector Radius', default='4', validators=[DataRequired()])
    n = FloatField('Neutron count', default='1E7', validators=[DataRequired()])
    submit = SubmitField('Run')
