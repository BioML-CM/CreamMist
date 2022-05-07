from flask import Blueprint,render_template,redirect,url_for, Response
from myproject import db
from myproject.models import Experiment, DoseResponse, JagsSampling, SensitivityScore
from myproject.cell_line.forms import CellLineForm, ChoiceForm, Logistic_Form, InputForm

from flask import request

import scipy.stats as stats
from myproject.cell_line import plot_data
from scipy.stats import skewnorm
import numpy as np
import pandas as pd
import json
import plotly


cell_line_search_blueprint = Blueprint('cell_line_search',
                                __name__,template_folder='templates/cell_line')

@cell_line_search_blueprint.route('/', methods=['GET', 'POST'])
def select():  #choose cell line
    form = CellLineForm()
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        return redirect(url_for('cell_line.information_cell_line', cell_line=name, dataset='All'))
    return render_template('search.html',form=form)


@cell_line_search_blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    cell_line_name_db = ["Olongapo City",
              "Angeles City",
              "Manila",
              "Makati",
              "Pasig",
              "Davao",
              "Cebu",
              "Quezon City",
              "Taguig"]
    print(cities)
    return Response(json.dumps(cell_line_name_db), mimetype='application/json')