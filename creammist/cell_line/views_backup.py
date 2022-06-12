from flask import Blueprint, render_template, redirect, url_for
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore
from creammist.cell_line.forms import AddForm, ChoiceForm, Logistic_Form, InputForm

import scipy.stats as stats
from creammist.cell_line import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly

cell_line_blueprint = Blueprint('cell_line',
                                __name__, template_folder='templates/cell_line')

hdi = 0.95
random_state = 1


# @cell_line_blueprint.route('/')
# def index():
#     print('Hello HI')
#     data = db.session.query(Exp,JagsSampling).join(Exp).all()
#     return render_template('home.html', data=data)

@cell_line_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose cell line
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for('cell_line.information_cell_line', cell_line=name, dataset='All'))
    return render_template('select_cell_line.html', form=form)


@cell_line_blueprint.route("/<string:dataset>/<string:cell_line>", methods=['GET', 'POST'])
def information_cell_line(cell_line, dataset):  # show information cell line
    # all dataset
    cell_line_records = db.session.query(Experiment.dataset).filter(
        Experiment.standard_cell_line_name == cell_line).distinct()

    # form for select dataset
    form = ChoiceForm()
    form.dataset.choices = [r.dataset for r in cell_line_records]

    if form.validate_on_submit():
        dataset = form.dataset.data
        return redirect(url_for('cell_line.information_cell_line', cell_line=cell_line, dataset=dataset))

    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(
        Experiment.standard_cell_line_name == cell_line, Experiment.dataset == dataset)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)

    # plot graph
    fig_ic50 = plot_data.plot_ic_auc_mode(df, 'ic50')
    fig_ic90 = plot_data.plot_ic_auc_mode(df, 'ic90')
    fig_auc = plot_data.plot_ic_auc_mode(df, 'auc')

    graph1Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('information_cell_line.html', data=data, graph1Jason=graph1Jason, graph2Jason=graph2Jason,
                           graph3Jason=graph3Jason, form=form, cell_line=cell_line, dataset=dataset)


@cell_line_blueprint.route("/view/<string:exp>/<string:input_dose>", methods=['GET', 'POST'])
def view_logistic(exp, input_dose):
    experiment = Experiment.query.filter_by(id=exp).first()
    jags = JagsSampling.query.filter_by(exp_id=exp).first()
    dose_list = DoseResponse.query.filter_by(exp_id=exp).all()

    c = str(experiment.standard_cell_line_name)
    drug = str(experiment.standard_drug_name)
    # dataset = experiment.dataset

    # all dataset
    cell_line_records = db.session.query(Experiment.dataset).filter(Experiment.standard_cell_line_name == c,
                                                                    Experiment.standard_drug_name == drug).distinct()
    print([r.dataset for r in cell_line_records])
    # form for select dataset
    form = Logistic_Form()
    form.dataset.choices = [r.dataset for r in cell_line_records]

    # form for input dose
    form1 = InputForm()

    if form.validate_on_submit():
        dataset = form.dataset.data
        exp_records = db.session.query(Experiment.id).filter(Experiment.standard_cell_line_name == c,
                                                             Experiment.standard_drug_name == drug,
                                                             Experiment.dataset == dataset).first()
        for e in exp_records:
            exp = e
        return redirect(url_for('cell_line.view_logistic', exp=exp, input_dose=input_dose))

    if form1.validate_on_submit():
        input_dose = form1.value.data
        return redirect(url_for('cell_line.view_logistic', exp=exp, input_dose=input_dose))

    dosage = []
    response = []
    dataset = []
    for d in dose_list:
        dosage += [d.dosage]
        response += [d.response]
        dataset += [Experiment.query.filter_by(id=d.exp_id).first().dataset]

    # Sampling
    n_sampling = 10000
    beta0_s = stats.skewnorm(jags.beta0_skew, jags.beta0_mu, jags.beta0_sigma).rvs(n_sampling,
                                                                                   random_state=random_state)
    beta1_s = stats.skewnorm(jags.beta1_skew, jags.beta1_mu, jags.beta1_sigma).rvs(n_sampling,
                                                                                   random_state=random_state)

    auc_list = []
    for i in range(n_sampling):
        auc = plot_data.find_auc(np.log2(jags.min_dosage), np.log2(jags.max_dosage), beta1_s[i], beta0_s[i])
        if ~np.isfinite(auc):
            auc_list += [0]
        else:
            auc_list += [auc]

    ic90_list = []
    ic50_list = []
    input_dose_list = []
    input_dose = np.float(input_dose)

    for i in range(n_sampling):
        ic90_list += [plot_data.inv_logistic(0.9, beta1_s[i], beta0_s[i])]
        ic50_list += [plot_data.inv_logistic(0.5, beta1_s[i], beta0_s[i])]
        input_dose_list += [plot_data.logistic(np.log2(input_dose), beta1_s[i], beta0_s[i])]

    fig_logistic = plot_data.plot_logistic(jags, beta0_s, beta1_s, dosage, response, dataset)
    fig_auc = plot_data.plot_distribution(auc_list, 0.01, hdi, 'AUC')
    fig_ic90 = plot_data.plot_distribution(ic90_list, 1, hdi, 'IC90')
    fig_ic50 = plot_data.plot_distribution_ic50(ic50_list, 1, jags)
    fig_input_dose = plot_data.plot_distribution(input_dose_list, 0.01, hdi, f'{input_dose}->{np.log2(input_dose):.2f}')

    graph1Jason = json.dumps(fig_logistic, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph4Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)
    graph5Jason = json.dumps(fig_input_dose, cls=plotly.utils.PlotlyJSONEncoder)

    print(experiment.info)
    return render_template('view_cell_line.html', experiment=experiment, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason,
                           graph3Jason=graph3Jason, graph4Jason=graph4Jason, graph5Jason=graph5Jason, form=form,
                           form1=form1)
