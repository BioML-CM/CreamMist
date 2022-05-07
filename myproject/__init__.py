import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))


# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/creammist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Migrate(app,db)

# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"
from myproject.cell_line.views import cell_line_blueprint
from myproject.drug.views import drug_blueprint
from myproject.cancer_type.views import cancer_type_blueprint
from myproject.biomarker.views import biomarker_blueprint
from myproject.gene.views import gene_blueprint

app.register_blueprint(cell_line_blueprint,url_prefix="/cell_line")
app.register_blueprint(drug_blueprint,url_prefix="/drug")
app.register_blueprint(cancer_type_blueprint,url_prefix="/cancer_type")
app.register_blueprint(biomarker_blueprint,url_prefix="/biomarker")
app.register_blueprint(gene_blueprint,url_prefix="/gene")

# from myproject.cell_line.views_test import cell_line_search_blueprint
# app.register_blueprint(cell_line_search_blueprint,url_prefix="/cell_line_search")