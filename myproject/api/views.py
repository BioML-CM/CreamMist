from flask import Blueprint,render_template,redirect,url_for, Response
from myproject import db
from myproject.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine
from myproject.cell_line.forms import CellLineForm, DatasetChoiceForm, DatasetLogisticForm, InputForm

from flask import request, send_file, jsonify

from myproject.cell_line import plot_data
import numpy as np
import pandas as pd
import json
import plotly


api_blueprint = Blueprint('api',
                              __name__,template_folder='templates/api')



@api_blueprint.route('/<string:dataset>/<string:cell_line>', methods=['GET'])
def get_cl_info(cell_line,dataset):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.cellosaurus_id == cell_line, Experiment.dataset == dataset)#.all()

    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['cellosaurus_id', 'standard_drug_name','dataset','info','n_dosage','min_dosage','max_dosage',
             'ic50_mode','ic90_calculate','ec50_calculate','einf_calculate','auc_calculate','fitted_mae']]
    df = df.rename(columns={'ic50_mode':'IC50','ic90_calculate':'IC90','ec50_calculate':'EC50',
                       'einf_calculate':'Einf','auc_calculate':'AUC'})
    result = df.to_json(orient="records")
    return result

@api_blueprint.route('/ic50/<string:dataset>/<string:cancer_type>', methods=['GET'])
def get_ct_ic50(dataset, cancer_type):
    if cancer_type=='pancan':
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).all()
    else:
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).filter(CellLine.site == cancer_type).all()
    cell_line_list = [r.cellosaurus_id for r in cancer_type_records]

    data = db.session.query(Experiment, SensitivityScore) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.cellosaurus_id.in_(cell_line_list), Experiment.dataset == dataset) #.all()

    df = pd.read_sql(data.statement, db.session.bind)
    df['cancer_type'] = cancer_type
    df = df[['cancer_type','cellosaurus_id','standard_drug_name','dataset','info',
             'ic50_mode','ic90_calculate','ec50_calculate','einf_calculate','auc_calculate']]
    df = df.rename(columns={'ic50_mode':'IC50','ic90_calculate':'IC90','ec50_calculate':'EC50',
                            'einf_calculate':'Einf','auc_calculate':'AUC'})
    result = df.to_json(orient="records")
    return result

@api_blueprint.route('/<string:drug>/<string:dataset>', methods=['GET','POST'])
def get_drug_info(drug,dataset):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.standard_drug_name == drug, Experiment.dataset == dataset) #.all()

    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['standard_drug_name','cellosaurus_id' ,'dataset','info','n_dosage','min_dosage','max_dosage',
             'ic50_mode','ic90_calculate','ec50_calculate','einf_calculate','auc_calculate','fitted_mae']]
    df = df.rename(columns={'ic50_mode':'IC50','ic90_calculate':'IC90','ec50_calculate':'EC50',
                            'einf_calculate':'Einf','auc_calculate':'AUC'})
    result = df.to_json(orient="records")
    return result

@api_blueprint.route('/drug_express/<string:drug>/<string:dataset>', methods=['GET','POST'])
def get_drug_express(drug,dataset):
    express_data = db.session.query(GeneExpression).filter(GeneExpression.standard_drug_name == drug, GeneExpression.dataset == dataset, GeneExpression.cancer_type == 'pancan')#.all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    express_df = express_df[['standard_drug_name','gene','dataset','cancer_type','correlation','pvalue','n_cell_line']]
    result = express_df.to_json(orient="records")
    return result

@api_blueprint.route('/drug_mutation/<string:drug>/<string:dataset>', methods=['GET','POST'])
def get_drug_mutation(drug,dataset):
    mutation_data = db.session.query(Mutation).filter(Mutation.standard_drug_name == drug, Mutation.dataset == dataset, Mutation.cancer_type == 'pancan')#.all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    mutation_df = mutation_df.rename(columns={'statistic':'effect_size', 'provided_statistic':'provided_effect_size'})

    mutation_df = mutation_df[['standard_drug_name','gene','dataset','cancer_type','effect_size','pvalue','n_mut','n_wt']]

    result = mutation_df.to_json(orient="records")
    return result

@api_blueprint.route('/gene_mutation/<string:dataset>/<string:gene>/<string:cancer_type>', methods=['GET','POST'])
def get_gene_mutation(gene, dataset, cancer_type):
    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.dataset == dataset, Mutation.cancer_type == cancer_type)#.all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)

    mutation_df = mutation_df[['gene','standard_drug_name','dataset','cancer_type','statistic','pvalue','n_mut','n_wt']]
    mutation_df = mutation_df.rename(columns={'statistic':'effect_size'})
    result = mutation_df.to_json(orient="records")
    return result

@api_blueprint.route('/gene_expression/<string:dataset>/<string:gene>/<string:cancer_type>', methods=['GET','POST'])
def get_gene_express(gene, dataset, cancer_type):

    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene, GeneExpression.dataset == dataset, GeneExpression.cancer_type == cancer_type)#.all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)

    express_df = express_df[['gene','standard_drug_name','dataset','cancer_type','correlation','pvalue','n_cell_line']]
    result = express_df.to_json(orient="records")
    return result

@api_blueprint.route('/biomarker/<string:drug>/<string:gene>/<string:cancer_type>', methods=['GET','POST'])
def get_biomarker_info(gene, drug, cancer_type):
    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.standard_drug_name == drug, Mutation.cancer_type == cancer_type)#.all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    mutation_df = mutation_df[['dataset','statistic','pvalue','provided_statistic','provided_pvalue']]
    mutation_df = mutation_df.rename(columns={'statistic':'effect_size_mutation', 'provided_statistic':'provided_effect_size_mutation',
                                              'pvalue':'pvalue_mutation',  'provided_pvalue': 'provided_pvalue_mutation'})

    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene, GeneExpression.standard_drug_name == drug, GeneExpression.cancer_type == cancer_type)#.all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    express_df = express_df[['dataset','correlation','pvalue','provided_correlation','provided_pvalue']]
    express_df = express_df.rename(columns={'correlation':'correlation_expression', 'provided_correlation':'provided_correlation_expression',
                                            'pvalue':'pvalue_expression',  'provided_pvalue': 'provided_pvalue_expression'})

    df = pd.merge(mutation_df,express_df,on=['dataset'],how='outer')

    result = df.to_json(orient="records")
    return result