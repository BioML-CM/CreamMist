from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine, MutExpMetadata, Drug, \
    Gene, GeneExpression, Mutation

from flask import request, send_file, jsonify

import numpy as np
import pandas as pd
import json
import plotly

# var_df = pd.read_csv('myproject/biomarker/data/mutation.csv', index_col=0)
# gene_express_df = pd.read_csv('myproject/biomarker/data/gene_expression.csv', index_col=0)


api_blueprint = Blueprint('api',
                          __name__, template_folder='templates/api')


@api_blueprint.route('/information/', methods=['GET', 'POST'])
def information():  # choose cell line
    return render_template('information_api.html')


@api_blueprint.route('/celllines', methods=['GET'])
def get_all_celllines_data():
    data = db.session.query(CellLine)
    df = pd.read_sql(data.statement, db.session.bind)
    result = df.to_json(orient="records")
    return result


@api_blueprint.route('/celllines/<string:cell_line>', methods=['GET'])
def get_drug_with_cl_info(cell_line):
    data = db.session.query(Experiment).filter(Experiment.cellosaurus_id == cell_line)  # .all()
    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['cellosaurus_id', 'standard_drug_name', 'dataset', 'info']]
    if df.shape[0] > 0:
        result = df.to_json(orient="records")
        return result, 200
    else:
        return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/cancertypes', methods=['GET'])
def get_all_cancertypes_data():
    data = db.session.query(CellLine.site).distinct()
    df = pd.read_sql(data.statement, db.session.bind)
    df.loc[len(df.index)] = 'pancan'
    df = df[df['site'] != '']
    result = json.dumps({"cancer_types": list(df['site'])})  # df.to_json(orient="values")
    return result


@api_blueprint.route('/cancertypes/<string:cancer_type>', methods=['GET'])
def get_cl_with_cancertypes(cancer_type):
    if cancer_type == 'pancan':
        data = db.session.query(CellLine.cellosaurus_id)
    else:
        data = db.session.query(CellLine.cellosaurus_id).filter(CellLine.site == cancer_type)
    df = pd.read_sql(data.statement, db.session.bind)
    if df.shape[0] > 0:
        result = json.dumps({"cell_lines": list(df['cellosaurus_id'])})
        return result, 200
    else:
        return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/experiments/<string:cell_line>/<string:drug>', methods=['GET'])
def get_experiments(cell_line, drug):
    data = db.session.query(Experiment, JagsSampling, SensitivityScore) \
        .join(JagsSampling, JagsSampling.exp_id == Experiment.id) \
        .join(SensitivityScore, SensitivityScore.exp_id == Experiment.id).filter(Experiment.cellosaurus_id == cell_line,
                                                                                 Experiment.standard_drug_name == drug)  # .all()

    df = pd.read_sql(data.statement, db.session.bind)

    exp_id_list = list(df[df['dataset'] != 'All']['exp_id'])

    list_of_dose_list = []

    for _, row in df.iterrows():
        if row['dataset'] == 'All':
            dose_list = db.session.query(DoseResponse).filter(DoseResponse.exp_id.in_(exp_id_list)).all()
        else:
            dose_list = DoseResponse.query.filter_by(exp_id=row['exp_id']).all()
        list_of_dose_list += [[(d.dosage, d.response) for d in dose_list]]
    df.loc[:, 'dose_response'] = list_of_dose_list

    df = df[['cellosaurus_id', 'standard_drug_name', 'dataset', 'info', 'n_dosage', 'min_dosage', 'max_dosage',
             'dose_response', 'ic50_mode', 'ic90_calculate', 'ec50_calculate', 'einf_calculate', 'auc_calculate',
             'fitted_mae']]
    # print(df)
    df = df.rename(columns={'ic50_mode': 'IC50', 'ic90_calculate': 'IC90', 'ec50_calculate': 'EC50',
                            'einf_calculate': 'Einf', 'auc_calculate': 'AUC'})
    result = df.to_json(orient="records")
    return result


@api_blueprint.route('/drugs', methods=['GET'])
def get_all_drug_data():
    data = db.session.query(Drug)
    df = pd.read_sql(data.statement, db.session.bind)
    result = df.to_json(orient="records")
    return result


@api_blueprint.route('/drugs/<string:drug>', methods=['GET'])
def get_cl_with_drug_info(drug):
    data = db.session.query(Experiment).filter(Experiment.standard_drug_name == drug)  # .all()
    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['standard_drug_name', 'cellosaurus_id', 'dataset', 'info']]
    if df.shape[0] > 0:
        result = df.to_json(orient="records")
        return result, 200
    else:
        return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/genes', methods=['GET'])
def get_all_genes_data():
    data = db.session.query(Gene).distinct()
    df = pd.read_sql(data.statement, db.session.bind)
    result = json.dumps({'genes': list(df['gene_name'])})  # df.to_json(orient="values")
    return result


@api_blueprint.route(
    '/biomarker/<string:exp_mut>/<string:cancer_type>/gene/<string:gene>/<string:pos_neg>/<string:n_top>',
    methods=['GET'])
def get_gene_express_mut(exp_mut, cancer_type, gene, pos_neg, n_top):
    if exp_mut == 'exp':
        express_data = db.session.query(GeneExpression).filter(GeneExpression.cancer_type == cancer_type,
                                                               GeneExpression.gene == gene,
                                                               GeneExpression.dataset == 'All')  # .all()
        df = pd.read_sql(express_data.statement, db.session.bind)
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'correlation', 'pvalue', 'n_cell_line']]
        if pos_neg == 'pos':
            df = df[df['correlation'] >= 0].sort_values(by='correlation', ascending=False).head(int(n_top))
        elif pos_neg == 'neg':
            df = df[df['correlation'] <= 0].sort_values(by='correlation', ascending=True).head(int(n_top))

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404

    elif exp_mut == 'mut':
        mutation_data = db.session.query(Mutation).filter(Mutation.cancer_type == cancer_type, Mutation.gene == gene,
                                                          Mutation.dataset == 'All')  # .all()
        df = pd.read_sql(mutation_data.statement, db.session.bind)
        df = df.rename(columns={'statistic': 'effect_size', 'provided_statistic': 'provided_effect_size'})
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'effect_size', 'pvalue', 'n_mut', 'n_wt']]

        if pos_neg == 'pos':
            df = df[df['effect_size'] >= 0].sort_values(by='effect_size', ascending=False).head(int(n_top))
        elif pos_neg == 'neg':
            df = df[df['effect_size'] <= 0].sort_values(by='effect_size', ascending=True).head(int(n_top))

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route(
    '/biomarker/<string:exp_mut>/<string:cancer_type>/drug/<string:drug>/<string:pos_neg>/<string:n_top>',
    methods=['GET'])
def get_drug_express_mut(exp_mut, cancer_type, drug, pos_neg, n_top):
    if exp_mut == 'exp':
        express_data = db.session.query(GeneExpression).filter(GeneExpression.cancer_type == cancer_type,
                                                               GeneExpression.standard_drug_name == drug,
                                                               GeneExpression.dataset == 'All')  # .all()
        df = pd.read_sql(express_data.statement, db.session.bind)
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'correlation', 'pvalue', 'n_cell_line']]
        if pos_neg == 'pos':
            df = df[df['correlation'] >= 0].sort_values(by='correlation', ascending=False).head(int(n_top))
        elif pos_neg == 'neg':
            df = df[df['correlation'] <= 0].sort_values(by='correlation', ascending=True).head(int(n_top))

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404

    elif exp_mut == 'mut':
        mutation_data = db.session.query(Mutation).filter(Mutation.cancer_type == cancer_type,
                                                          Mutation.standard_drug_name == drug,
                                                          Mutation.dataset == 'All')  # .all()
        df = pd.read_sql(mutation_data.statement, db.session.bind)
        df = df.rename(columns={'statistic': 'effect_size', 'provided_statistic': 'provided_effect_size'})
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'effect_size', 'pvalue', 'n_mut', 'n_wt']]

        if pos_neg == 'pos':
            df = df[df['effect_size'] >= 0].sort_values(by='effect_size', ascending=False).head(int(n_top))
        elif pos_neg == 'neg':
            df = df[df['effect_size'] <= 0].sort_values(by='effect_size', ascending=True).head(int(n_top))

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/biomarker/<string:exp_mut>/<string:cancer_type>/info/<string:gene>/<string:drug>',
                     methods=['GET'])
def get_drug_gene_express_mut(exp_mut, cancer_type, gene, drug):
    if exp_mut == 'exp':
        express_data = db.session.query(GeneExpression).filter(GeneExpression.gene == gene,
                                                               GeneExpression.standard_drug_name == drug,
                                                               GeneExpression.dataset == 'All',
                                                               GeneExpression.cancer_type == cancer_type)  # .all()
        df = pd.read_sql(express_data.statement, db.session.bind)
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'correlation', 'pvalue', 'n_cell_line']]

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404

    elif exp_mut == 'mut':
        mutation_data = db.session.query(Mutation).filter(Mutation.gene == gene, Mutation.standard_drug_name == drug,
                                                          Mutation.dataset == 'All',
                                                          Mutation.cancer_type == cancer_type)  # .all()
        df = pd.read_sql(mutation_data.statement, db.session.bind)
        df = df.rename(columns={'statistic': 'effect_size', 'provided_statistic': 'provided_effect_size'})
        df = df[['standard_drug_name', 'gene', 'dataset', 'cancer_type', 'effect_size', 'pvalue', 'n_mut', 'n_wt']]

        if df.shape[0] > 0:
            result = df.to_json(orient="records")
            return result, 200
        else:
            return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/mutation/<string:cell_line>/', methods=['GET'])
def get_cl_mutation(cell_line):
    cell_line_records = db.session.query(CellLine.cellosaurus_index).filter(
        CellLine.cellosaurus_id == cell_line).distinct()
    cell_line_list = [c.cellosaurus_index for c in cell_line_records]
    print(cell_line_list)

    data = db.session.query(MutExpMetadata).filter(MutExpMetadata.cellosaurus_index == cell_line_list[0],
                                                   MutExpMetadata.score == 'mutation')  # .all()
    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['gene', 'values']]

    if df.shape[0] > 0:
        result = df.to_json(orient="records")
        return result, 200
    else:
        return jsonify({"message": "404 Not Found"}), 404


@api_blueprint.route('/expression/<string:cell_line>/', methods=['GET'])
def get_cl_express(cell_line):
    cell_line_records = db.session.query(CellLine.cellosaurus_index).filter(
        CellLine.cellosaurus_id == cell_line).distinct()
    cell_line_list = [c.cellosaurus_index for c in cell_line_records]

    data = db.session.query(MutExpMetadata).filter(MutExpMetadata.cellosaurus_index == cell_line_list[0],
                                                   MutExpMetadata.score == 'gene_expression')  # .all()
    df = pd.read_sql(data.statement, db.session.bind)
    df = df[['gene', 'values']]

    if df.shape[0] > 0:
        result = df.to_json(orient="records")
        return result, 200
    else:
        return jsonify({"message": "404 Not Found"}), 404
