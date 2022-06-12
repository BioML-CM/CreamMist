from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine, Mutation, \
    GeneExpression, Gene
from creammist.gene.forms import GeneForm, ChoiceForm

from flask import request, send_file

import scipy.stats as stats
from creammist.gene import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly

gene_blueprint = Blueprint('gene',
                           __name__, template_folder='templates/gene')


@gene_blueprint.route('/download_mutation/<string:dataset>/<string:gene>/<string:cancer_type>', methods=['GET', 'POST'])
def download_mutation(gene, dataset, cancer_type):
    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.dataset == dataset,
                                                      Mutation.cancer_type == cancer_type)  # .all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)

    mutation_df = mutation_df[
        ['gene', 'standard_drug_name', 'dataset', 'cancer_type', 'statistic', 'pvalue', 'n_mut', 'n_wt']]
    mutation_df = mutation_df.rename(columns={'statistic': 'effect_size'})
    path = f'gene/output/mutation_{gene}_{cancer_type}_{dataset}_information.csv'
    mutation_df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@gene_blueprint.route('/download_expression/<string:dataset>/<string:gene>/<string:cancer_type>',
                      methods=['GET', 'POST'])
def download_expression(gene, dataset, cancer_type):
    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                           GeneExpression.dataset == dataset,
                                                           GeneExpression.cancer_type == cancer_type)  # .all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)

    express_df = express_df[
        ['gene', 'standard_drug_name', 'dataset', 'cancer_type', 'correlation', 'pvalue', 'n_cell_line']]
    path = f'gene/output/gene_expression_{gene}_{cancer_type}_{dataset}_information.csv'
    express_df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@gene_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    gene_records = db.session.query(Gene.gene_name).all()
    gene_name_db = [r.gene_name for r in gene_records]

    return Response(json.dumps(gene_name_db), mimetype='application/json')


@gene_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose cell line
    form = GeneForm()
    if request.method == 'POST':
        gene = request.form.get('name')
        return redirect(url_for('gene.information_gene', gene=gene, dataset='All', cancer_type='pancan'))
    return render_template('select_gene.html', form=form)


@gene_blueprint.route("/<string:dataset>/<string:gene>/<string:cancer_type>", methods=['GET', 'POST'])
def information_gene(gene, dataset, cancer_type):  # show information cell line

    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.dataset == dataset,
                                                      Mutation.cancer_type == cancer_type)  # .all()
    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                           GeneExpression.dataset == dataset,
                                                           GeneExpression.cancer_type == cancer_type)  # .all()

    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    # print(mutation_df.shape)

    # all dataset
    gene_mutation_records = db.session.query(Mutation).filter(Mutation.gene == gene)  # .all()
    dataset_mutation_list = list(set(r.dataset for r in gene_mutation_records))
    cancer_type_mutation_list = list(set(r.cancer_type for r in gene_mutation_records))

    gene_exprees_records = db.session.query(GeneExpression).filter(GeneExpression.gene == gene)  # .all()
    dataset_exprees_list = list(set(r.dataset for r in gene_exprees_records))
    cancer_type_express_list = list(set(r.cancer_type for r in gene_exprees_records))

    dataset_list = sorted(list(set(dataset_mutation_list).union(set(dataset_exprees_list))))
    cancer_type_list = sorted(list(set(cancer_type_mutation_list).union(set(cancer_type_express_list))))

    # form for select dataset
    form = ChoiceForm()
    form.dataset.choices = [(d, d) for d in dataset_list]
    form.cancer_type.choices = [(c, c) for c in cancer_type_list]

    form.dataset.default = dataset
    form.cancer_type.default = cancer_type
    form.process()

    if request.method == 'POST':
        dataset = request.form.get('dataset')
        cancer_type = request.form.get('cancer_type')
        # score = request.form.get('score')
        return redirect(url_for('gene.information_gene', gene=gene, dataset=dataset, cancer_type=cancer_type))

    # plot graph
    if mutation_df.shape[0] > 0:
        fig_mutation_stat = plot_data.plot_statistic(mutation_df, 'statistic')
        graph1Jason = json.dumps(fig_mutation_stat, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph1Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)

    if express_df.shape[0] > 0:
        fig_express_stat = plot_data.plot_statistic(express_df, 'correlation')
        graph2Jason = json.dumps(fig_express_stat, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph2Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('information_gene.html', data=mutation_data, form=form, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason,
                           gene=gene, dataset=dataset, cancer_type=cancer_type)

# @gene_blueprint.route("/<string:dataset>/<string:cancer_type>/<string:gene>/<string:score>",methods=['GET', 'POST'])
# def information_gene(gene, dataset, score, cancer_type): #show information cell line
#
#     if score == 'mutation':
#         data = db.session.query(WildtypeMutation).filter(WildtypeMutation.gene == gene, WildtypeMutation.dataset == dataset, WildtypeMutation.cancer_type == cancer_type)#.all()
#     elif score == 'gene expression':
#         data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene, GeneExpression.dataset == dataset, GeneExpression.cancer_type == cancer_type)#.all()
#
#     df = pd.read_sql(data.statement, db.session.bind)
#     print(data.statement)
#
#
#     #all dataset
#
#     gene_records = db.session.query(WildtypeMutation).filter(WildtypeMutation.gene == gene)#.all()
#     dataset_list = list(set(r.dataset for r in gene_records))
#     cancer_type_list = list(set(r.cancer_type for r in gene_records))
#
#     #form for select dataset
#     form = ChoiceForm()
#     form.dataset.choices = dataset_list
#     form.cancer_type.choices = cancer_type_list
#
#     form.dataset.default = dataset
#     form.cancer_type.default = cancer_type
#     form.process()
#
#     if request.method == 'POST':
#         dataset = request.form.get('dataset')
#         cancer_type = request.form.get('cancer_type')
#         score = request.form.get('score')
#         return redirect(url_for('gene.information_gene', gene=gene, dataset=dataset, cancer_type=cancer_type, score=score))
#
#     print(df)
#     #plot graph
#     if score == 'mutation':
#         fig_stat = plot_data.plot_statistic(df,'statistic')
#         fig_stat_provided = plot_data.plot_statistic(df,'statistic_provided')
#     elif score == 'gene expression':
#         fig_stat = plot_data.plot_statistic(df,'correlation')
#         fig_stat_provided = plot_data.plot_statistic(df,'correlation_provided')
#
#     graph1Jason = json.dumps(fig_stat, cls=plotly.utils.PlotlyJSONEncoder)
#     graph2Jason = json.dumps(fig_stat_provided, cls=plotly.utils.PlotlyJSONEncoder)
#
#
#     return render_template('information_gene.html', data=data, graph1Jason=graph1Jason,form=form,
#                            graph2Jason=graph2Jason, score=score, gene=gene, dataset=dataset, cancer_type=cancer_type)