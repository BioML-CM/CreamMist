from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine
from creammist.cell_line.forms import CellLineForm, DatasetChoiceForm, DatasetLogisticForm, InputForm

from flask import request, send_file

from creammist.cell_line import plot_data
import numpy as np
import pandas as pd
import json
import plotly

cell_line_blueprint = Blueprint('cell_line',
                                __name__, template_folder='templates/cell_line')

hdi = 0.95
random_state = 1


@cell_line_blueprint.route('/download/<string:dataset>/<string:cell_line>', methods=['GET', 'POST'])
def download(cell_line, dataset):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.cellosaurus_id == cell_line,
                                                                                 Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['cellosaurus_id', 'standard_drug_name', 'dataset', 'info', 'n_dosage', 'min_dosage', 'max_dosage',
             'ic50_mode', 'ic90_calculate', 'ec50_calculate', 'einf_calculate', 'auc_calculate']]
    df = df.rename(columns={'ic50_mode': 'IC50', 'ic90_calculate': 'IC90', 'ec50_calculate': 'EC50',
                            'einf_calculate': 'Einf', 'auc_calculate': 'AUC', 'info':'original_datasets',
                            'standard_drug_name':'drug_name'})
    path = f'cell_line/output/cell_line_{cell_line}_{dataset}_information.csv'
    df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@cell_line_blueprint.route('/download_experiment/<string:exp>', methods=['GET', 'POST'])
def download_experiment(exp):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.id == exp)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)

    cl = str(df['cellosaurus_id'].values[0])
    drug = str(df['standard_drug_name'].values[0])

    # all dataset
    cell_line_records = db.session.query(Experiment).filter(Experiment.cellosaurus_id == cl,
                                                            Experiment.standard_drug_name == drug).distinct()

    exp_id_list = []
    for r in cell_line_records:
        if r.dataset != 'All':
            exp_id_list += [r.id]


    list_of_dose_list = []

    for _, row in df.iterrows():
        if row['dataset'] == 'All':
            dose_list = db.session.query(DoseResponse).filter(DoseResponse.exp_id.in_(exp_id_list)).all()
        else:
            dose_list = DoseResponse.query.filter_by(exp_id=row['exp_id']).all()
        list_of_dose_list += [[(d.dosage, d.response) for d in dose_list]]
    df.loc[:, 'dose_response'] = list_of_dose_list

    df = df[['cellosaurus_id', 'standard_drug_name', 'dataset', 'info', 'n_dosage', 'min_dosage', 'max_dosage',
             'dose_response','fitted_mae','beta1_mode', 'ic50_mode', 'ic90_calculate', 'ec50_calculate', 'einf_calculate',
             'auc_calculate',]]
    # print(df)
    df = df.rename(columns={'ic50_mode': 'IC50', 'ic90_calculate': 'IC90', 'ec50_calculate': 'EC50',
                            'einf_calculate': 'Einf', 'auc_calculate': 'AUC','info':'original_datasets','beta1_mode':'slope',
                            'standard_drug_name':'drug_name'})

    path = f'cell_line/output/experiment_{cl}_{drug}_information.csv'
    df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@cell_line_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    cell_line_records = db.session.query(Experiment.cellosaurus_id).distinct()
    cell_line_name_db = [r.cellosaurus_id for r in cell_line_records]

    return Response(json.dumps(cell_line_name_db), mimetype='application/json')


@cell_line_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose cell line
    cell_line_records = db.session.query(Experiment.cellosaurus_id).distinct()
    cell_line_name_db = [r.cellosaurus_id for r in cell_line_records]

    form = CellLineForm()
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('cell_line.information_cell_line', cell_line=name, dataset='All'))
    return render_template('select_cell_line.html', form=form, data=cell_line_name_db)


@cell_line_blueprint.route("/<string:dataset>/<string:cell_line>", methods=['GET', 'POST'])
def information_cell_line(cell_line, dataset):  # show information cell line

    # form for select dataset
    cell_line_dataset_records = db.session.query(Experiment.dataset).filter(
        Experiment.cellosaurus_id == cell_line).distinct()

    form = DatasetChoiceForm()
    form.dataset.choices = [(r.dataset, r.dataset) for r in sorted(cell_line_dataset_records)]
    form.dataset.default = dataset
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        return redirect(url_for('cell_line.information_cell_line', cell_line=cell_line, dataset=dataset))

    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.cellosaurus_id == cell_line,
                                                                                 Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)

    # plot graph
    fig_ic50 = plot_data.plot_ic_auc_mode(df, 'ic50')
    fig_ic90 = plot_data.plot_ic_auc_mode(df, 'ic90')
    fig_auc = plot_data.plot_ic_auc_mode(df, 'auc')

    graph1Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)

    # name cell line in each dataset (for information)
    cell_line_info_records = db.session.query(CellLine).filter(CellLine.cellosaurus_id == cell_line).all()
    cell_line_info = [c for c in cell_line_info_records]
    cell_line_info = cell_line_info[0]
    name_dict = dict()
    if cell_line_info.ccle_name != '':
        name_dict['CCLE'] = cell_line_info.ccle_name
    if cell_line_info.ctrp1_name != '':
        name_dict['CTRP1'] = cell_line_info.ctrp1_name
    if cell_line_info.ctrp2_name != '':
        name_dict['CTRP2'] = cell_line_info.ctrp2_name
    if cell_line_info.gdsc1_name != '':
        name_dict['GDSC1'] = cell_line_info.gdsc1_name
    if cell_line_info.gdsc2_name != '':
        name_dict['GDSC2'] = cell_line_info.gdsc2_name

    name_list = []
    for val in set(name_dict.values()):
        key = [k for k, v in name_dict.items() if v == val]
        name_list += [[key, val]]

    return render_template('information_cell_line.html', data=data, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason, graph3Jason=graph3Jason, form=form, dataset=dataset,
                           cell_line_info=cell_line_info, name_list=name_list, cell_line=cell_line)


@cell_line_blueprint.route("/view/<string:exp>", methods=['GET', 'POST'])
def view_logistic(exp):
    experiment = Experiment.query.filter_by(id=exp).first()
    jags = JagsSampling.query.filter_by(exp_id=exp).first()
    sens = SensitivityScore.query.filter_by(exp_id=exp).all()

    c = str(experiment.cellosaurus_id)
    drug = str(experiment.standard_drug_name)
    dataset = experiment.dataset

    # all dataset
    cell_line_records = db.session.query(Experiment).filter(Experiment.cellosaurus_id == c,
                                                            Experiment.standard_drug_name == drug).distinct()
    dataset_list = []
    exp_id_list = []
    for r in cell_line_records:
        dataset_list += [(r.dataset, r.dataset)]
        if r.dataset != 'All':
            exp_id_list += [r.id]

    # form for select dataset
    form = DatasetLogisticForm()
    form.dataset.choices = dataset_list
    form.dataset.default = dataset
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        exp_records = db.session.query(Experiment.id).filter(Experiment.cellosaurus_id == c,
                                                             Experiment.standard_drug_name == drug,
                                                             Experiment.dataset == dataset).first()
        for e in exp_records:
            exp = e
        return redirect(url_for('cell_line.view_logistic', exp=exp))

    if dataset == 'All':
        dose_list = db.session.query(DoseResponse).filter(DoseResponse.exp_id.in_(exp_id_list)).all()
    else:
        dose_list = DoseResponse.query.filter_by(exp_id=exp).all()

    dosage = []
    response = []
    dataset_plot = []
    for d in dose_list:
        dosage += [d.dosage]
        response += [d.response]
        dataset_plot += [Experiment.query.filter_by(id=d.exp_id).first().dataset]

    beta0_s = np.array(jags.beta0_jags_str.split(',')).astype(float)
    beta1_s = np.array(jags.beta1_jags_str.split(',')).astype(float)

    ic50_list = []
    for i in range(len(beta0_s)):
        ic50_list += [plot_data.inv_logistic(0.5, beta1_s[i], beta0_s[i])]

    fig_logistic = plot_data.plot_logistic1(jags, sens, beta0_s, beta1_s, dosage, response, dataset_plot)
    # fig_auc = plot_data.plot_distribution(auc_list,0.01,hdi,'AUC')
    # fig_ic90 = plot_data.plot_distribution(ic90_list,1,hdi,'IC90')
    fig_ic50 = plot_data.plot_distribution_ic50(ic50_list, jags.beta0_HDI_low, jags.beta0_HDI_high)
    # fig_input_dose = plot_data.plot_distribution(input_dose_list,0.01,hdi,f'{input_dose}->{np.log2(input_dose):.2f}')

    graph1Jason = json.dumps(fig_logistic, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    # graph3Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    # graph4Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)
    # graph5Jason = json.dumps(fig_input_dose, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('view_cell_line.html', experiment=experiment, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason, form=form, data=sens,cl=c,drug=drug)
