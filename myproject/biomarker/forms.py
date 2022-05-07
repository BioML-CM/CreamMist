from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField, HiddenField

class BiomarkerForm(FlaskForm):

    gene_name = StringField('Gene :', id='biomarker_autocomplete')
    drug_name = StringField('Standard drug name :', id='biomarker_autocomplete_drug')
    # hidden_name = HiddenField(id='hidden')


class ChoiceForm(FlaskForm):
    score = SelectField('Select score', choices=['mutation', 'gene expression'])
    cancer_type = SelectField('Select Cancer Type', choices=[])
    # submit = SubmitField('Enter')
