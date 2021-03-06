from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, Drug, Mutation, GeneExpression
from creammist.drug.forms import DrugForm, DatasetChoiceForm

from flask import request, send_file

import scipy.stats as stats
from creammist.drug import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly

drug_blueprint = Blueprint('drug', __name__, template_folder='templates/drug')

hdi = 0.95
random_state = 1


@drug_blueprint.route('/download/<string:drug>/<string:dataset>', methods=['GET', 'POST'])
def download(drug, dataset):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.standard_drug_name == drug,
                                                                                 Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['standard_drug_name', 'cellosaurus_id', 'dataset', 'info', 'n_dosage', 'min_dosage', 'max_dosage',
             'ic50_mode', 'ic90_calculate', 'ec50_calculate', 'einf_calculate', 'auc_calculate']]
    df = df.rename(columns={'ic50_mode': 'IC50', 'ic90_calculate': 'IC90', 'ec50_calculate': 'EC50',
                            'einf_calculate': 'Einf', 'auc_calculate': 'AUC','info':'original_datasets',
                            'standard_drug_name':'drug_name'})
    path = f'drug/output/drug_{drug}_{dataset}_information.csv'
    df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@drug_blueprint.route('/download_express/<string:drug>/<string:dataset>', methods=['GET', 'POST'])
def download_express(drug, dataset):
    express_data = db.session.query(GeneExpression).filter(GeneExpression.standard_drug_name == drug,
                                                           GeneExpression.dataset == dataset,
                                                           GeneExpression.cancer_type == 'pancan')  # .all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    express_df = express_df[
        ['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'correlation', 'pvalue', 'n_cell_line']]
    express_df = express_df.rename(columns={'standard_drug_name':'drug_name'})

    path = f'drug/output/gene_expression_{drug}_{dataset}_pancan_information.csv'
    express_df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@drug_blueprint.route('/download_mutation/<string:drug>/<string:dataset>', methods=['GET', 'POST'])
def download_mutation(drug, dataset):
    mutation_data = db.session.query(Mutation).filter(Mutation.standard_drug_name == drug, Mutation.dataset == dataset,
                                                      Mutation.cancer_type == 'pancan')  # .all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    mutation_df = mutation_df.rename(columns={'statistic': 'effect_size', 'provided_statistic': 'provided_effect_size',
                                              'standard_drug_name':'drug_name'})

    mutation_df = mutation_df[
        ['drug_name', 'gene', 'dataset', 'cancer_type', 'effect_size', 'pvalue', 'n_mut', 'n_wt']]

    path = f'drug/output/mutation_{drug}_{dataset}_pancan_information.csv'
    mutation_df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@drug_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    drug_records = db.session.query(Experiment.standard_drug_name).distinct()
    drug_name_db = [r.standard_drug_name for r in drug_records]

    return Response(json.dumps(drug_name_db), mimetype='application/json')


@drug_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose drug
    drug_records = db.session.query(Experiment.standard_drug_name).distinct()
    drug_name_db = [r.standard_drug_name for r in drug_records]

    form = DrugForm()
    if request.method == 'POST':
        name = request.form.get('name')
        if name in drug_name_db:
            return redirect(url_for('drug.information_drug', drug=name, dataset='All'))
        else:
            return render_template('select_drug.html', form=form, data=drug_name_db)
    return render_template('select_drug.html', form=form, data=drug_name_db)


@drug_blueprint.route("/<string:dataset>/<string:drug>", methods=['GET', 'POST'])
def information_drug(drug, dataset):  # show information cell line

    # all dataset
    drug_records = db.session.query(Experiment.dataset).filter(Experiment.standard_drug_name == drug).distinct()

    # form for select dataset
    form = DatasetChoiceForm()
    form.dataset.choices = [(r.dataset, r.dataset) for r in sorted(drug_records)]
    form.dataset.default = dataset
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        return redirect(url_for('drug.information_drug', drug=drug, dataset=dataset))

    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.standard_drug_name == drug,
                                                                                 Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)
    drug = pd.unique(df['standard_drug_name'])[0]

    mutation_data = db.session.query(Mutation).filter(Mutation.standard_drug_name == drug, Mutation.dataset == dataset,
                                                      Mutation.cancer_type == 'pancan')  # .all()
    express_data = db.session.query(GeneExpression).filter(GeneExpression.standard_drug_name == drug,
                                                           GeneExpression.dataset == dataset,
                                                           GeneExpression.cancer_type == 'pancan')  # .all()

    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    # print(mutation_df)
    # print(express_df)

    # plot graph
    fig_ic50 = plot_data.plot_ic_auc_mode(df, 'ic50')
    fig_ic90 = plot_data.plot_ic_auc_mode(df, 'ic90')
    fig_auc = plot_data.plot_ic_auc_mode(df, 'auc')
    fig_mutation = plot_data.plot_statistic(mutation_df, 'statistic')
    fig_gene_expression = plot_data.plot_statistic(express_df, 'correlation')

    graph1Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)
    graph4Jason = json.dumps(fig_mutation, cls=plotly.utils.PlotlyJSONEncoder)
    graph5Jason = json.dumps(fig_gene_expression, cls=plotly.utils.PlotlyJSONEncoder)

    # name each dataset
    drug_info_records = db.session.query(Drug).filter(Drug.standard_drug_name == drug).all()
    drug_info = [d for d in drug_info_records]
    drug_info = drug_info[0]
    name_dict = dict()
    if drug_info.ccle_drug_name != '':
        name_dict['CCLE'] = drug_info.ccle_drug_name
    if drug_info.ctrp1_drug_name != '':
        name_dict['CTRP1'] = drug_info.ctrp1_drug_name
    if drug_info.ctrp2_drug_name != '':
        name_dict['CTRP2'] = drug_info.ctrp2_drug_name
    if drug_info.gdsc1_drug_name != '':
        name_dict['GDSC1'] = drug_info.gdsc1_drug_name
    if drug_info.gdsc2_drug_name != '':
        name_dict['GDSC2'] = drug_info.gdsc2_drug_name
    # print(set(name_dict.values()))
    name_list = []
    for val in set(name_dict.values()):
        key = [k for k, v in name_dict.items() if v == val]
        name_list += [[key, val]]
    # print(name_list)

    return render_template('information_drug.html', data=data, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason, graph3Jason=graph3Jason, graph4Jason=graph4Jason,
                           graph5Jason=graph5Jason, form=form,
                           dataset=dataset, drug_info=drug_info, name_list=name_list, drug=drug)
