from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField

class CancerForm(FlaskForm):

    name = StringField('Cancer Type :' , id='cancer_type_autocomplete')
    # submit = SubmitField('Enter')

class DatasetChoiceForm(FlaskForm):
    dataset = SelectField('Select dataset', choices=[])
    submit = SubmitField('Enter')