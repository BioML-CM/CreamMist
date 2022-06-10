from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField


class GeneForm(FlaskForm):
    name = StringField('Gene :', id='gene_autocomplete')
    # drug_name = StringField('Standard drug name :', id='biomarker_autocomplete_drug')


class ChoiceForm(FlaskForm):
    score = SelectField('Select score', choices=['mutation', 'gene expression'])
    dataset = SelectField('Dataset', choices=[])
    cancer_type = SelectField('Cancer Type', choices=[])
    # submit = SubmitField('Enter')
