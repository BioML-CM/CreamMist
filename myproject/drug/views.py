from flask import Blueprint,render_template,redirect,url_for,Response
from myproject import db
from myproject.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, Drug
from myproject.drug.forms import DrugForm, DatasetChoiceForm

from flask import request

import scipy.stats as stats
from myproject.drug import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly


drug_blueprint = Blueprint('drug',__name__,template_folder='templates/drug')



hdi=0.95
random_state=1

# @cell_line_blueprint.route('/')
# def index():
#     print('Hello HI')
#     data = db.session.query(Exp,JagsSampling).join(Exp).all()
#     return render_template('home.html', data=data)
@drug_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    drug_records = db.session.query(Experiment.standard_drug_name).distinct()
    drug_name_db = [r.standard_drug_name for r in drug_records]

    return Response(json.dumps(drug_name_db), mimetype='application/json')


@drug_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  #choose drug
    form = DrugForm()
    if request.method == 'POST':
        name = request.form.get('name')
        # print(name)
        return redirect(url_for('drug.information_drug', drug=name, dataset='All'))
    return render_template('select_drug.html',form=form)



@drug_blueprint.route("/<string:dataset>/<string:drug>",methods=['GET', 'POST'])
def information_drug(drug, dataset): #show information cell line

    #all dataset
    drug_records = db.session.query(Experiment.dataset).filter(Experiment.standard_drug_name == drug).distinct()

    #form for select dataset
    form = DatasetChoiceForm()
    form.dataset.choices = [(r.dataset, r.dataset) for r in sorted(drug_records)]
    form.dataset.default = dataset
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        return redirect(url_for('drug.information_drug', drug=drug, dataset=dataset))


    data = db.session.query(Experiment, JagsSampling, SensitivityScore)\
            .join(JagsSampling, JagsSampling.exp_id == Experiment.id)\
            .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.standard_drug_name == drug, Experiment.dataset == dataset) #.all()

    df = pd.read_sql(data.statement, db.session.bind)
    drug = pd.unique(df['standard_drug_name'])[0]

    #plot graph
    fig_ic50 = plot_data.plot_ic_auc_mode(df,'ic50')
    fig_ic90 = plot_data.plot_ic_auc_mode(df,'ic90')
    fig_auc = plot_data.plot_ic_auc_mode(df,'auc')

    graph1Jason = json.dumps(fig_ic50, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_ic90, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_auc, cls=plotly.utils.PlotlyJSONEncoder)



    #name each dataset
    drug_info_records = db.session.query(Drug).filter(Drug.standard_drug_name == drug).all()
    drug_info = [d for d in drug_info_records]
    drug_info = drug_info[0]
    name_dict = dict()
    if drug_info.ccle_drug_name !='':
        name_dict['CCLE'] = drug_info.ccle_drug_name
    if drug_info.ctrp1_drug_name !='':
        name_dict['CTRP1'] = drug_info.ctrp1_drug_name
    if drug_info.ctrp2_drug_name !='':
        name_dict['CTRP2'] = drug_info.ctrp2_drug_name
    if drug_info.gdsc1_drug_name !='':
        name_dict['GDSC1'] = drug_info.gdsc1_drug_name
    if drug_info.gdsc2_drug_name !='':
        name_dict['GDSC2'] = drug_info.gdsc2_drug_name
    # print(set(name_dict.values()))
    name_list = []
    for val in set(name_dict.values()):
        key =  [k for k, v in name_dict.items() if v == val]
        name_list += [[key,val]]
    # print(name_list)

    return render_template('information_drug.html', data=data, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason, graph3Jason=graph3Jason, form=form,
                           dataset=dataset,drug_info=drug_info, name_list=name_list,drug=drug)

