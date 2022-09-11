import os
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))


# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://creammist:CreamMist$2022@13.213.238.8/creammist-2022-09" # mysql://username:password@server/db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set FLASK_APP=app.py
# flask db init (only for first time)
# flask db stamp head (only if database is not up to date)

# flask db migrate -m "first migration"
# flask db upgrade

db = SQLAlchemy(app)
Migrate(app, db, compare_type=True)

# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"
from creammist.cell_line.views import cell_line_blueprint
from creammist.drug.views import drug_blueprint
from creammist.cancer_type.views import cancer_type_blueprint
from creammist.biomarker.views import biomarker_blueprint
from creammist.gene.views import gene_blueprint
from creammist.api.views import api_blueprint
from creammist.doc.views import doc_blueprint

app.register_blueprint(cell_line_blueprint,url_prefix="/cell_line")
app.register_blueprint(drug_blueprint,url_prefix="/drug")
app.register_blueprint(cancer_type_blueprint,url_prefix="/cancer_type")
app.register_blueprint(biomarker_blueprint,url_prefix="/biomarker")
app.register_blueprint(gene_blueprint,url_prefix="/gene")
app.register_blueprint(api_blueprint,url_prefix="/api")
app.register_blueprint(doc_blueprint,url_prefix="/doc")

# from myproject.cell_line.views_test import cell_line_search_blueprint
# app.register_blueprint(cell_line_search_blueprint,url_prefix="/cell_line_search")
