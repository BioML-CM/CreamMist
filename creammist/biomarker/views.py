from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine, Mutation, \
    GeneExpression, Gene, OmicsProfiles
from creammist.biomarker.forms import BiomarkerForm, ChoiceForm

from flask import request, send_file

from creammist.biomarker import plot_data
import pandas as pd
import json
import plotly


biomarker_blueprint = Blueprint('biomarker',
                                __name__, template_folder='templates/biomarker')


@biomarker_blueprint.route('/download/<string:drug>/<string:gene>/<string:cancer_type>', methods=['GET', 'POST'])
def download(gene, drug, cancer_type):
    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.standard_drug_name == drug,
                                                      Mutation.cancer_type == cancer_type)  # .all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)
    mutation_df = mutation_df[['dataset', 'statistic', 'pvalue', 'provided_statistic', 'provided_pvalue']]
    mutation_df = mutation_df.rename(
        columns={'statistic': 'creammist_effect_size_mutation', 'provided_statistic': 'original_source_effect_size_mutation',
                 'pvalue': 'creammist_pvalue_mutation', 'provided_pvalue': 'original_source_pvalue_mutation'})

    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                           GeneExpression.standard_drug_name == drug,
                                                           GeneExpression.cancer_type == cancer_type)  # .all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)
    express_df = express_df[['dataset', 'correlation', 'pvalue', 'provided_correlation', 'provided_pvalue']]
    express_df = express_df.rename(
        columns={'correlation': 'creammist_correlation_expression', 'provided_correlation': 'original_source_correlation_expression',
                 'pvalue': 'creammist_pvalue_expression', 'provided_pvalue': 'original_source_pvalue_expression'})

    df = pd.merge(mutation_df, express_df, on=['dataset'], how='outer')

    path = f'gene/output/biomarker_{gene}_{drug}_{cancer_type}_information.csv'
    df.to_csv('creammist/' + path, index=False)
    return send_file(path, as_attachment=True)


@biomarker_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():

    gene_records = db.session.query(Gene.gene_name).all()
    gene_name_db = [r.gene_name for r in gene_records]
    return Response(json.dumps(gene_name_db), mimetype='application/json')


@biomarker_blueprint.route('/_autocomplete_drug', methods=['GET'])
def autocomplete_drug():
    gene = request.args.get('gene')
    # print(gene)
    # print(request.form.get('hidden_name'))
    drug_mutation_records = db.session.query(Mutation.standard_drug_name).filter(Mutation.gene == gene).distinct()
    drug_express_records = db.session.query(GeneExpression.standard_drug_name).filter(
        GeneExpression.gene == gene).distinct()

    drug_mutation_list = [r.standard_drug_name for r in drug_mutation_records]
    drug_express_list = [r.standard_drug_name for r in drug_express_records]

    drug_name_db = list(set(drug_mutation_list).union(set(drug_express_list)))
    # print(drug_name_db)

    # drug_name_db = [r.standard_drug_name for r in drug_records]

    return Response(json.dumps(drug_name_db), mimetype='application/json')


@biomarker_blueprint.route('/select/', methods=['GET', 'POST'])
def select():  # choose cell line
    form = BiomarkerForm()
    if request.method == 'POST':
        gene_name = request.form.get('gene_name')
        drug_name = request.form.get('drug_name')

        drug_mutation_records = db.session.query(Mutation.standard_drug_name).filter(Mutation.gene == gene_name, Mutation.standard_drug_name == drug_name).distinct()
        drug_express_records = db.session.query(GeneExpression.standard_drug_name).filter(GeneExpression.gene == gene_name,GeneExpression.standard_drug_name == drug_name).distinct()
        drug_mutation_list = [r.standard_drug_name for r in drug_mutation_records]
        drug_express_list = [r.standard_drug_name for r in drug_express_records]

        if len(drug_mutation_list)!=0 or len(drug_express_list)!=0 :
            return redirect(
            url_for('biomarker.information_biomarker', gene=gene_name, drug=drug_name, cancer_type='pancan'))
        else:
            return render_template('select_biomarker.html', form=form)
    return render_template('select_biomarker.html', form=form)


@biomarker_blueprint.route("/<string:gene>/<string:drug>/<string:cancer_type>", methods=['GET', 'POST'])
def information_biomarker(gene, drug, cancer_type):

    mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.standard_drug_name == drug,
                                                      Mutation.cancer_type == cancer_type)  # .all()
    mutation_df = pd.read_sql(mutation_data.statement, db.session.bind)

    express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                           GeneExpression.standard_drug_name == drug,
                                                           GeneExpression.cancer_type == cancer_type)  # .all()
    express_df = pd.read_sql(express_data.statement, db.session.bind)


    # all dataset
    mutation_records = db.session.query(Mutation).filter(Mutation.gene == gene,
                                                         Mutation.standard_drug_name == drug)  # .all()
    cancer_type_mutation_list = list(set(r.cancer_type for r in mutation_records))

    express_records = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                              GeneExpression.standard_drug_name == drug)  # .all()
    cancer_type_express_list = list(set(r.cancer_type for r in express_records))

    cancer_type_list = list(set(cancer_type_mutation_list).union(set(cancer_type_express_list)))

    # form for select dataset
    form = ChoiceForm()
    form.cancer_type.choices = [(c, c) for c in cancer_type_list]
    form.cancer_type.default = cancer_type
    form.process()

    if request.method == 'POST':
        cancer_type = request.form.get('cancer_type')
        return redirect(url_for('biomarker.information_biomarker', gene=gene, drug=drug, cancer_type=cancer_type))

    # plot graph
    fig_mutation_stat, box_plot, mut_plot = plot_data.plot_mutation(mutation_df)
    fig_express_stat, scatt_plot, exp_plot = plot_data.plot_expression(express_df)
    if mut_plot:
        graph1Jason = json.dumps(fig_mutation_stat, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph1Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)

    if exp_plot:
        graph2Jason = json.dumps(fig_express_stat, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph2Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)


    # plot information
    # find cell line match cancer type
    if cancer_type == 'pancan':
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).all()
    else:
        cancer_type_records = db.session.query(CellLine.cellosaurus_id).filter(CellLine.site == cancer_type).all()
    cell_line_list = [r.cellosaurus_id for r in cancer_type_records]


    # find ic50
    data = db.session.query(CellLine, Experiment, JagsSampling) \
        .join(Experiment, Experiment.cellosaurus_id == CellLine.cellosaurus_id) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id).filter(Experiment.standard_drug_name == drug,
                                                                         Experiment.dataset == 'All')  # .all()
    df = pd.read_sql(data.statement, db.session.bind)
    df = df[df['cellosaurus_id'].isin(cell_line_list)]
    df = df[['cellosaurus_id', 'standard_drug_name', 'beta0_mode']]


    # find mut/exp values
    mut_exp_data = db.session.query(OmicsProfiles).filter(OmicsProfiles.gene == gene)  # .all()
    mut_exp_df = pd.read_sql(mut_exp_data.statement, db.session.bind)

    mut_exp_df = mut_exp_df[mut_exp_df['cellosaurus_id'].isin(cell_line_list)]
    mut_exp_df = mut_exp_df[['cellosaurus_id', 'gene', 'values', 'score']]


    if box_plot:
        fig_box_mutation = plot_data.plot_box_mutation(df, mut_exp_df)
        graph3Jason = json.dumps(fig_box_mutation, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph3Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)


    if scatt_plot:
        fig_scatter_expression = plot_data.plot_scatter_expression(df, mut_exp_df)
        graph4Jason = json.dumps(fig_scatter_expression, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph4Jason = json.dumps(plot_data.plot_nodata(), cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('information_biomarker.html', data=mutation_data, graph1Jason=graph1Jason,
                           graph2Jason=graph2Jason,
                           graph3Jason=graph3Jason, graph4Jason=graph4Jason, form=form, gene=gene, drug=drug,
                           cancer_type=cancer_type)
