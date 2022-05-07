from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField

class CellLineForm(FlaskForm):

    name = StringField('Cell Line Name :', id='cell_line_autocomplete')
    # submit = SubmitField('Enter')

class DatasetChoiceForm(FlaskForm):
    dataset = SelectField('Select Dataset', choices=[])
    # submit = SubmitField('Enter')

class DatasetLogisticForm(FlaskForm):
    dataset = SelectField('Select Dataset', choices=[])
    # submit = SubmitField('Enter')

class InputForm(FlaskForm):

    value = FloatField('Dose Value :')
    submit = SubmitField('Enter')