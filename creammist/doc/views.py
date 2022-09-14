from flask import Blueprint, render_template, redirect, url_for, Response


from flask import request, send_file


doc_blueprint = Blueprint('doc',
                          __name__, template_folder='templates/doc')


@doc_blueprint.route('/information/', methods=['GET', 'POST'])
def information():
    return render_template('overall_doc.html')


@doc_blueprint.route('/cell_line/', methods=['GET', 'POST'])
def cell_line():
    return render_template('cell_line_doc.html')


@doc_blueprint.route('/drug/', methods=['GET', 'POST'])
def drug():
    return render_template('drug_doc.html')


@doc_blueprint.route('/cancer_type/', methods=['GET', 'POST'])
def cancer_type():
    return render_template('cancer_type_doc.html')


@doc_blueprint.route('/gene/', methods=['GET', 'POST'])
def gene():
    return render_template('gene_doc.html')


@doc_blueprint.route('/biomarker/', methods=['GET', 'POST'])
def biomarker():
    return render_template('biomarker_doc.html')

@doc_blueprint.route('/dose_response_curve/', methods=['GET', 'POST'])
def dose_response_curve():
    return render_template('dose_response_curve_doc.html')

@doc_blueprint.route('/bulk_download/', methods=['GET', 'POST'])
def download_bulk():
    path = f'doc/bulk_download/bulk_download.csv'
    return send_file(path, as_attachment=True)


@doc_blueprint.route('/bulk/', methods=['GET', 'POST'])
def bulk():
    return render_template('bulk_doc.html')