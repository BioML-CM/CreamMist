from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine
from creammist.cancer_type.forms import CancerForm, DatasetChoiceForm

from flask import request, send_file

from creammist.cancer_type import plot_data

import pandas as pd
import json
import plotly
# import upsetplot
# from upsetplot import from_contents
from matplotlib import pyplot as plt

cancer_type_blueprint = Blueprint('cancer_type',
                                  __name__, template_folder='templates/cancer_type')


@cancer_type_blueprint.route('/download_ic50/<string:dataset>/<string:cancer_type>', methods=['GET', 'POST'])
def download(dataset, cancer_type):
    if cancer_type == 'pancan':
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).all()
    else:
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).filter(CellLine.site == cancer_type).all()
    cell_line_list = [r.cellosaurus_id for r in cancer_type_records]

    data = db.session.query(Experiment, SensitivityScore) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(
        Experiment.cellosaurus_id.in_(cell_line_list), Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)
    df['cancer_type'] = cancer_type
    df = df[['cancer_type', 'cellosaurus_id', 'standard_drug_name', 'dataset', 'info',
             'ic50_mode', 'ic90_calculate', 'ec50_calculate', 'einf_calculate', 'auc_calculate']]
    df = df.rename(columns={'ic50_mode': 'IC50', 'ic90_calculate': 'IC90', 'ec50_calculate': 'EC50',
                            'einf_calculate': 'Einf', 'auc_calculate': 'AUC'})
    path = f'cancer_type/output/cancer_type_{cancer_type}_{dataset}_information.csv'
    df.to_csv('myproject/' + path)
    return send_file(path, as_attachment=True)


@cancer_type_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    cellline_record = db.session.query(Experiment.cellosaurus_id).distinct()
    cellline_list = [r.cellosaurus_id for r in cellline_record]

    cancer_type_records = db.session.query(CellLine.site).filter(CellLine.cellosaurus_id.in_(cellline_list)).distinct()
    cancer_type_name_db = [r.site for r in cancer_type_records] + ['pancan']

    return Response(json.dumps(cancer_type_name_db), mimetype='application/json')


@cancer_type_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose cell line
    form = CancerForm()
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('cancer_type.information_cancer_type', cancer_type=name, dataset='All'))
    return render_template('select_cancer_type.html', form=form)


@cancer_type_blueprint.route("/<string:dataset>/<string:cancer_type>", methods=['GET', 'POST'])
def information_cancer_type(cancer_type, dataset):  # show information cell line
    # all dataset
    if cancer_type == 'pancan':
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).all()
    else:
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).filter(CellLine.site == cancer_type).all()
    cell_line_list = [r.cellosaurus_id for r in cancer_type_records]

    data = db.session.query(Experiment, SensitivityScore) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(
        Experiment.cellosaurus_id.in_(cell_line_list), Experiment.dataset == dataset)  # .all()
    # print(data.statement)

    dataset_records = db.session.query(Experiment.dataset).filter(
        Experiment.cellosaurus_id.in_(cell_line_list)).distinct()

    df = pd.read_sql(data.statement, db.session.bind)

    df = df[df['dataset'] == dataset]

    dataset_list = [(r.dataset, r.dataset) for r in
                    sorted(dataset_records)]  # sorted(dataset_list, key=lambda x: temp_list.index(x))

    # form for select dataset
    form = DatasetChoiceForm()
    form.dataset.choices = dataset_list
    form.dataset.default = dataset
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        return redirect(url_for('cancer_type.information_cancer_type', cancer_type=cancer_type, dataset=dataset))

    # print('plot')
    # plot graph
    fig_ic50 = plot_data.plot_ic_auc_mode(df, 'ic50_mode')
    fig_ic90 = plot_data.plot_ic_auc_mode(df, 'ic90_calculate')
    fig_auc = plot_data.plot_ic_auc_mode(df, 'auc_calculate')
    # print('after plot')
    graph1Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('information_cancer_type.html', data=data, graph1Jason=graph1Jason, graph2Jason=graph2Jason,
                           graph3Jason=graph3Jason, form=form, cancer_type=cancer_type, dataset=dataset)
