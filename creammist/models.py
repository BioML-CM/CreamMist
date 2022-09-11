from creammist import db


class CellLine(db.Model):
    __tablename__ = 'cell_lines'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cellosaurus_id = db.Column(db.String(64), primary_key=True)
    cellosaurus_index = db.Column(db.String(64)) #, index=True
    ccle_name = db.Column(db.String(64))
    ctrp1_name = db.Column(db.String(64))
    ctrp2_name = db.Column(db.String(64))
    gdsc1_name = db.Column(db.String(64))
    gdsc2_name = db.Column(db.String(64))
    site = db.Column(db.String(128)) #, index=True
    # Connect the exp.
    # cellosaurus_id = db.Column(db.String(64), db.ForeignKey('experiments.cellosaurus_id'), nullable=False, )

    experiments_of_cell_line = db.relationship('Experiment', backref='cell_line', lazy='dynamic')

    def __init__(self, site, cellosaurus_id, cellosaurus_index, ccle_name, ctrp1_name, ctrp2_name, gdsc1_name,
                 gdsc2_name):
        self.site = site
        self.ccle_name = ccle_name
        self.ctrp1_name = ctrp1_name
        self.ctrp2_name = ctrp2_name
        self.gdsc1_name = gdsc1_name
        self.gdsc2_name = gdsc2_name
        self.cellosaurus_index = cellosaurus_index
        self.cellosaurus_id = cellosaurus_id


class Drug(db.Model):
    __tablename__ = 'drugs'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    standard_drug_name = db.Column(db.String(64), primary_key=True, )
    synonyms = db.Column(db.String(128))
    target = db.Column(db.String(64))
    pathway = db.Column(db.String(256))
    ccle_drug_name = db.Column(db.String(64))
    ctrp1_drug_name = db.Column(db.String(64))
    ctrp2_drug_name = db.Column(db.String(64))
    gdsc1_drug_name = db.Column(db.String(64))
    gdsc2_drug_name = db.Column(db.String(64))

    experiments_of_drug = db.relationship('Experiment', backref='drug', lazy='dynamic')
    mutations = db.relationship('Mutation', backref='drug', lazy='dynamic')
    gene_expressions = db.relationship('GeneExpression', backref='drug', lazy='dynamic')

    # Connect the exp.
    # standard_drug_name = db.Column(db.String(64), db.ForeignKey('experiments.standard_drug_name'), nullable=False)  #

    def __init__(self, synonyms, target, pathway, standard_drug_name,
                 ccle_drug_name, ctrp1_drug_name, ctrp2_drug_name, gdsc1_drug_name, gdsc2_drug_name):
        self.synonyms = synonyms
        self.target = target
        self.pathway = pathway
        self.ccle_drug_name = ccle_drug_name
        self.ctrp1_drug_name = ctrp1_drug_name
        self.ctrp2_drug_name = ctrp2_drug_name
        self.gdsc1_drug_name = gdsc1_drug_name
        self.gdsc2_drug_name = gdsc2_drug_name
        self.standard_drug_name = standard_drug_name


class Experiment(db.Model):
    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    cellosaurus_id = db.Column(db.String(64), db.ForeignKey('cell_lines.cellosaurus_id'), nullable=False)
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('drugs.standard_drug_name'), nullable=False)
    dataset = db.Column(db.String(32), nullable=False)
    info = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint('cellosaurus_id', 'standard_drug_name', 'dataset'),
    )

    # This is a one-to-many relationship
    # exp can have many dosage/response
    dose_responses = db.relationship('DoseResponse', backref='experiment', lazy='dynamic')
    jags_sampling = db.relationship('JagsSampling', backref='experiment', lazy='dynamic')
    sensitivity_score = db.relationship('SensitivityScore', backref='experiment', lazy='dynamic')
    provided_sensitivity_score = db.relationship('ProvidedSensitivityScore', backref='experiment', lazy='dynamic')

    # drug_table = db.relationship('DrugTable', backref='exp', lazy='dynamic')
    # cell_line_table = db.relationship('CellLineTable', backref='exp', lazy='dynamic')
    # mutation = db.relationship('Mutation', backref='experiment', lazy='dynamic')
    # gene_expression = db.relationship('GeneExpression', backref='experiment', lazy='dynamic')

    def __init__(self, cellosaurus_id, standard_drug_name, dataset, info):
        self.cellosaurus_id = cellosaurus_id
        self.standard_drug_name = standard_drug_name
        self.dataset = dataset
        self.info = info


class DoseResponse(db.Model):
    __tablename__ = 'dose_responses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dosage = db.Column(db.Float)
    response = db.Column(db.Float)
    # Connect the exp.
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)  #

    def __init__(self, dosage, response, exp_id):
        self.dosage = dosage
        self.response = response
        self.exp_id = exp_id


class JagsSampling(db.Model):
    __tablename__ = 'jags_samplings'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), primary_key=True, nullable=False)
    n_dosage = db.Column(db.Integer)
    min_dosage = db.Column(db.Float)
    max_dosage = db.Column(db.Float)
    beta0_mode = db.Column(db.Float)
    beta0_HDI_low = db.Column(db.Float)
    beta0_HDI_high = db.Column(db.Float)
    beta1_mode = db.Column(db.Float)
    beta1_HDI_low = db.Column(db.Float)
    beta1_HDI_high = db.Column(db.Float)
    ic90_mode = db.Column(db.Float)
    ic90_HDI_low = db.Column(db.Float)
    ic90_HDI_high = db.Column(db.Float)
    ec50_mode = db.Column(db.Float)
    ec50_HDI_low = db.Column(db.Float)
    ec50_HDI_high = db.Column(db.Float)
    einf_mode = db.Column(db.Float)
    einf_HDI_low = db.Column(db.Float)
    einf_HDI_high = db.Column(db.Float)
    auc_mode = db.Column(db.Float)
    auc_HDI_low = db.Column(db.Float)
    auc_HDI_high = db.Column(db.Float)
    fitted_mae = db.Column(db.Float)
    beta0_jags_str = db.Column(db.Text)
    beta1_jags_str = db.Column(db.Text)

    # Connect the exp.

    def __init__(self, n_dosage, min_dosage, max_dosage, beta0_mode, beta0_HDI_low, beta0_HDI_high, beta1_mode,
                 beta1_HDI_low, beta1_HDI_high, ic90_mode, ic90_HDI_low, ic90_HDI_high,
                 ec50_mode, ec50_HDI_low, ec50_HDI_high, ecinf_mode, ecinf_HDI_low, ecinf_HDI_high,
                 auc_mode, auc_HDI_low, auc_HDI_high, fitted_mae,
                 beta0_jags_str, beta1_jags_str, exp_id):
        self.n_dosage = n_dosage
        self.min_dosage = min_dosage
        self.max_dosage = max_dosage
        self.beta0_mode = beta0_mode
        self.beta0_HDI_low = beta0_HDI_low
        self.beta0_HDI_high = beta0_HDI_high
        self.beta1_mode = beta1_mode
        self.beta1_HDI_low = beta1_HDI_low
        self.beta1_HDI_high = beta1_HDI_high
        self.ic90_mode = ic90_mode
        self.ic90_HDI_low = ic90_HDI_low
        self.ic90_HDI_high = ic90_HDI_high
        self.ec50_mode = ec50_mode
        self.ec50_HDI_low = ec50_HDI_low
        self.ec50_HDI_high = ec50_HDI_high
        self.einf_mode = ecinf_mode
        self.einf_HDI_low = ecinf_HDI_low
        self.einf_HDI_high = ecinf_HDI_high
        self.auc_mode = auc_mode
        self.auc_HDI_low = auc_HDI_low
        self.auc_HDI_high = auc_HDI_high
        self.fitted_mae = fitted_mae
        self.beta0_jags_str = beta0_jags_str
        self.beta1_jags_str = beta1_jags_str

        self.exp_id = exp_id


class SensitivityScore(db.Model):
    __tablename__ = 'sensitivity_scores'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), primary_key=True, nullable=False)
    ic50_HDI_low = db.Column(db.Float)
    ic50_HDI_high = db.Column(db.Float)
    ic50_mode = db.Column(db.Float)
    ic90_calculate = db.Column(db.Float)
    ec50_calculate = db.Column(db.Float)
    einf_calculate = db.Column(db.Float)
    auc_calculate = db.Column(db.Float)

    # Connect the exp.
    # exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)

    def __init__(self, ic50_HDI_low, ic50_HDI_high, ic50_mode, ic90_calculate, ec50_calculate,
                 einf_calculate, auc_calculate, exp_id):
        self.ic50_HDI_low = ic50_HDI_low
        self.ic50_HDI_high = ic50_HDI_high
        self.ic50_mode = ic50_mode
        self.ic90_calculate = ic90_calculate
        self.ec50_calculate = ec50_calculate
        self.einf_calculate = einf_calculate
        self.auc_calculate = auc_calculate

        self.exp_id = exp_id


class ProvidedSensitivityScore(db.Model):
    __tablename__ = 'provided_sensitivity_scores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
    ic50_provided = db.Column(db.Float)
    auc_provided = db.Column(db.Float)

    # Connect the exp.
    # exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)

    def __init__(self, ic50_provided, auc_provided, exp_id):
        self.ic50_provided = ic50_provided
        self.auc_provided = auc_provided

        self.exp_id = exp_id


class Gene(db.Model):
    __tablename__ = 'genes'

    gene_name = db.Column(db.String(64), primary_key=True)

    def __init__(self, gene_name):
        self.gene_name = gene_name

    mutations = db.relationship('Mutation', backref='gene_mutations_ref', lazy='dynamic')
    gene_expressions = db.relationship('GeneExpression', backref='gene_gene_expressions_ref', lazy='dynamic')


class Mutation(db.Model):
    __tablename__ = 'mutations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('drugs.standard_drug_name'))
    gene = db.Column(db.String(64), db.ForeignKey('genes.gene_name'))
    dataset = db.Column(db.String(32)) #, index=True
    cancer_type = db.Column(db.String(64)) #, index=True
    pvalue = db.Column(db.Float)
    statistic = db.Column(db.Float)
    provided_pvalue = db.Column(db.Float)
    provided_statistic = db.Column(db.Float)
    n_mut = db.Column(db.Integer)
    n_wt = db.Column(db.Integer)
    provided_n_mut = db.Column(db.Integer)
    provided_n_wt = db.Column(db.Integer)

    def __init__(self, gene, dataset, cancer_type, pvalue, statistic, provided_pvalue, provided_statistic,
                 standard_drug_name, n_mut, n_wt, provided_n_mut, provided_n_wt):
        self.gene = gene
        self.dataset = dataset
        self.cancer_type = cancer_type
        self.pvalue = pvalue
        self.statistic = statistic
        self.provided_pvalue = provided_pvalue
        self.provided_statistic = provided_statistic
        self.standard_drug_name = standard_drug_name
        self.n_mut = n_mut
        self.n_wt = n_wt
        self.provided_n_mut = provided_n_mut
        self.provided_n_wt = provided_n_wt


class GeneExpression(db.Model):
    __tablename__ = 'gene_expressions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('drugs.standard_drug_name'))
    gene = db.Column(db.String(64), db.ForeignKey('genes.gene_name'))
    dataset = db.Column(db.String(32)) #, index=True
    cancer_type = db.Column(db.String(64)) #, index=True
    pvalue = db.Column(db.Float)
    correlation = db.Column(db.Float)
    provided_pvalue = db.Column(db.Float)
    provided_correlation = db.Column(db.Float)
    n_cell_line = db.Column(db.Integer)
    provided_n_cell_line = db.Column(db.Integer)

    # Connect the exp.
    # standard_drug_name = db.Column(db.String(64), db.ForeignKey('experiments.standard_drug_name'))  #

    def __init__(self, gene, dataset, cancer_type, pvalue, correlation, provided_pvalue, provided_correlation,
                 standard_drug_name, n_cell_line, provided_n_cell_line):
        self.gene = gene
        self.dataset = dataset
        self.cancer_type = cancer_type
        self.pvalue = pvalue
        self.correlation = correlation
        self.provided_pvalue = provided_pvalue
        self.provided_correlation = provided_correlation
        self.standard_drug_name = standard_drug_name
        self.n_cell_line = n_cell_line
        self.provided_n_cell_line = provided_n_cell_line

# For matrix factorization in the future
# class DrugSimilarity(db.Model):
#     __tablename__ = 'drug_similarities'
#
#     drug_x = db.Column(db.String(64), db.ForeignKey('drugs.standard_drug_name'), primary_key=True)
#     drug_y = db.Column(db.String(64), db.ForeignKey('drugs.standard_drug_name'), primary_key=True)
#     similarity = db.Column(db.Float)
#
#     def __init__(self, drug_x, drug_y, similarity):
#         self.drug_x = drug_x
#         self.drug_y = drug_y
#         self.similarity = similarity

# For matrix factorization in the future
# class GeneSimilarity(db.Model):
#     __tablename__ = 'gene_similarities'
#
#     gene_x = db.Column(db.String(64), db.ForeignKey('genes.gene_name'), primary_key=True)
#     gene_y = db.Column(db.String(64), db.ForeignKey('genes.gene_name'), primary_key=True)
#     similarity = db.Column(db.Float)
#
#     def __init__(self, gene_x, gene_y, similarity):
#         self.gene_x = gene_x
#         self.gene_y = gene_y
#         self.similarity = similarity

class OmicsProfiles(db.Model): #OmicsProfiles
    __tablename__ = 'omics_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cellosaurus_id = db.Column(db.String(64), db.ForeignKey('cell_lines.cellosaurus_id'), nullable=False)
    gene = db.Column(db.String(64), db.ForeignKey('genes.gene_name'))
    values = db.Column(db.Float)
    score = db.Column(db.String(64))

    def __init__(self, cellosaurus_id, gene, values, score):
        self.cellosaurus_id = cellosaurus_id
        self.gene = gene
        self.values = values
        self.score = score

# TO DELETE
# class MutExpMetadata(db.Model): #OmicsProfiles
#     __tablename__ = 'mut_exp_metadata'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cellosaurus_index = db.Column(db.String(64), nullable=False, index=True)
#     gene = db.Column(db.String(64), index=True)
#     values = db.Column(db.Float)
#     score = db.Column(db.String(64))
#
#     def __init__(self, cellosaurus_index, gene, values, score):
#         self.cellosaurus_index = cellosaurus_index
#         self.gene = gene
#         self.values = values
#         self.score = score
