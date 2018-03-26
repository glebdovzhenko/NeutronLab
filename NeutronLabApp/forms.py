from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class SimplePlotForm(FlaskForm):
    xs = StringField('x range', default='0,1', validators=[DataRequired()])
    submit = SubmitField('Run')


class PinholeSANSForm(FlaskForm):
    Lambda = FloatField('Wavelength', default='4.5', validators=[DataRequired()])
    DLambda = FloatField('Wavelength STD', default='0.1', validators=[DataRequired()])
    DistSrcPin1 = FloatField('Source to 1st slit', default='1', validators=[DataRequired()])
    DistSrcPin2 = FloatField('Source to 2nd slit', default='10', validators=[DataRequired()])
    DistPinSamp = FloatField('2nd slit to sample', default='1', validators=[DataRequired()])
    DistSampDet = FloatField('Sample to detector', default='10', validators=[DataRequired()])
    DetRadius = FloatField('Detector Radius', default='4', validators=[DataRequired()])
    n_count = FloatField('Neutron count', default='1E7', validators=[DataRequired()])
    submit = SubmitField('Run')
