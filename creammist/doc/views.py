from flask import Blueprint, render_template

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

@doc_blueprint.route('/dose_response_curve/', methods=['GET', 'POST'])
def dose_response_curve():  # choose cell line
    return render_template('dose_response_curve_doc.html')