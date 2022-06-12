from flask import Blueprint, render_template, redirect, url_for, Response
from creammist import db
from creammist.models import Experiment, DoseResponse, JagsSampling, SensitivityScore, CellLine, MutExpMetadata, Drug, \
    Gene, GeneExpression, Mutation

from flask import request, send_file, jsonify

import numpy as np
import pandas as pd
import json
import plotly

doc_blueprint = Blueprint('doc',
                          __name__, template_folder='templates/doc')


@doc_blueprint.route('/information/', methods=['GET', 'POST'])
def information():  # choose cell line
    return render_template('overall_doc.html')


@doc_blueprint.route('/cell_line/', methods=['GET', 'POST'])
def cell_line():  # choose cell line
    return render_template('cell_line_doc.html')


@doc_blueprint.route('/drug/', methods=['GET', 'POST'])
def drug():  # choose cell line
    return render_template('drug_doc.html')


@doc_blueprint.route('/cancer_type/', methods=['GET', 'POST'])
def cancer_type():  # choose cell line
    return render_template('cancer_type_doc.html')


@doc_blueprint.route('/gene/', methods=['GET', 'POST'])
def gene():  # choose cell line
    return render_template('gene_doc.html')


@doc_blueprint.route('/biomarker/', methods=['GET', 'POST'])
def biomarker():  # choose cell line
    return render_template('biomarker_doc.html')

@doc_blueprint.route('/ml_models/', methods=['GET', 'POST'])
def ml_models():  # choose cell line
    return render_template('ml_models_doc.html')