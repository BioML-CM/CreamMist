from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField

class DrugForm(FlaskForm):

    name = StringField('Drug Name :', id='drug_autocomplete')
    # submit = SubmitField('Enter')

class DatasetChoiceForm(FlaskForm):
    dataset = SelectField('Select Dataset', choices=[])
    # submit = SubmitField('Enter')

# class DatasetLogisticForm(FlaskForm):
#     dataset = SelectField('Select Dataset', choices=[])
    # submit = SubmitField('Enter')