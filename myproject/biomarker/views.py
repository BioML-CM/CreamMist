from flask import Blueprint,render_template,redirect,url_for, Response
from myproject import db
from myproject.models import Exp, DoseResponse, JagsSampling, Sensitive, CellLineTable, WildtypeMutation, GeneExpression
from myproject.biomarker.forms import BiomarkerForm, ChoiceForm

from flask import request

import scipy.stats as stats
from myproject.biomarker import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly


biomarker_blueprint = Blueprint('biomarker',
                              __name__,template_folder='templates/biomarker')



@biomarker_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    gene_mutation_records = db.session.query(WildtypeMutation.gene).distinct()
    gene_express_records = db.session.query(GeneExpression.gene).distinct()
    gene_mutation_list = [r.gene for r in gene_mutation_records]
    gene_express_list = [r.gene for r in gene_express_records]
    gene_name_db = list(set(gene_mutation_list).union(set(gene_express_list)))

    return Response(json.dumps(gene_name_db), mimetype='application/json')

@biomarker_blueprint.route('/_autocomplete_drug', methods=['GET'])
def autocomplete_drug():
    gene = request.args.get('gene')
    print(gene)
    # print(request.form.get('hidden_name'))
    drug_mutation_records = db.session.query(WildtypeMutation.standard_drug_name).filter(WildtypeMutation.gene == gene).distinct()
    drug_express_records = db.session.query(GeneExpression.standard_drug_name).filter(GeneExpression.gene == gene).distinct()

    drug_mutation_list = [r.standard_drug_name for r in drug_mutation_records]
    drug_express_list = [r.standard_drug_name for r in drug_express_records]
    drug_name_db = list(set(drug_mutation_list).union(set(drug_express_list)))


    # drug_name_db = [r.standard_drug_name for r in drug_records]

    return Response(json.dumps(drug_name_db), mimetype='application/json')


@biomarker_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  #choose cell line
    form = BiomarkerForm()
    if request.method == 'POST':
        gene_name = request.form.get('gene_name')
        drug_name = request.form.get('drug_name')
        return redirect(url_for('biomarker.information_biomarker', gene=gene_name, drug=drug_name,cancer_type='pancan'))
    return render_template('select_biomarker.html',form=form)



@biomarker_blueprint.route("/<string:cancer_type>/<string:gene>/<string:drug>",methods=['GET', 'POST'])
def information_biomarker(gene, drug, cancer_type): #show information cell line


    mutation_data = db.session.query(WildtypeMutation).filter(WildtypeMutation.gene == gene, WildtypeMutation.standard_drug_name == drug, WildtypeMutation.cancer_type == cancer_type)#.all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    mutation_df = mutation_df[['dataset','statistic','pvalue','statistic_provided','pvalue_provided']]

    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene, GeneExpression.standard_drug_name == drug, GeneExpression.cancer_type == cancer_type)#.all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    express_df = express_df[['dataset','correlation','pvalue','correlation_provided','pvalue_provided']]


    #all dataset
    mutation_records = db.session.query(WildtypeMutation).filter(WildtypeMutation.gene == gene, WildtypeMutation.standard_drug_name == drug)#.all()
    cancer_type_mutation_list = list(set(r.cancer_type for r in mutation_records))
    express_records = db.session.query(GeneExpression).filter(GeneExpression.gene == gene, GeneExpression.standard_drug_name == drug)#.all()
    cancer_type_express_list = list(set(r.cancer_type for r in express_records))

    cancer_type_list = list(set(cancer_type_mutation_list).union(set(cancer_type_express_list)))

    #form for select dataset
    form = ChoiceForm()
    form.cancer_type.choices = cancer_type_list
    form.cancer_type.default = cancer_type
    form.process()

    if request.method == 'POST':
        cancer_type = request.form.get('cancer_type')
        return redirect(url_for('biomarker.information_biomarker', gene=gene, drug=drug, cancer_type=cancer_type))

    print(express_df)
    #plot graph
    fig_mutation_stat = plot_data.plot_biomarker(mutation_df,'statistic','pvalue','Statistic')
    fig_mutation_stat_provided = plot_data.plot_biomarker(mutation_df,'statistic_provided','pvalue_provided','Statistic Provided')

    fig_express_stat = plot_data.plot_biomarker(express_df,'correlation','pvalue','Correlation')
    # fig_express_stat_provided = plot_data.plot_biomarker(express_df,'correlation_provided','pvalue','Correlation')

    graph1Jason = json.dumps(fig_mutation_stat, cls=plotly.utils.PlotlyJSONEncoder)
    graph2Jason = json.dumps(fig_mutation_stat_provided, cls=plotly.utils.PlotlyJSONEncoder)
    graph3Jason = json.dumps(fig_express_stat, cls=plotly.utils.PlotlyJSONEncoder)
    graph4Jason = json.dumps(fig_express_stat, cls=plotly.utils.PlotlyJSONEncoder)


    # if score == 'mutation':
    #     fig_statistic = plot_data.plot_biomarker(df,'statistic','pvalue','Statistic')
    #     fig_statistic_prov = plot_data.plot_biomarker(df,'statistic_provided','pvalue_provided','Statistic Provided')
    # elif score == 'gene expression':
    #
    #     fig_statistic = plot_data.plot_biomarker(df,'correlation','pvalue','Correlation')
    #     # fig_statistic_prov = plot_data.plot_biomarker(df,'correlation_provided','pvalue_provided','Correlation Provided')
    #
    # graph1Jason = json.dumps(fig_statistic, cls=plotly.utils.PlotlyJSONEncoder)
    # graph2Jason = json.dumps(fig_statistic, cls=plotly.utils.PlotlyJSONEncoder)

    #
    #
    return render_template('information_biomarker.html', data=mutation_data, graph1Jason=graph1Jason, graph2Jason=graph2Jason,
                           graph3Jason=graph3Jason, graph4Jason=graph4Jason,form=form, gene=gene, drug=drug, cancer_type=cancer_type)


