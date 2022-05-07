from myproject import db


class Exp(db.Model):
    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cellosaurus_index = db.Column(db.String(64), nullable=False)
    cellosaurus_id = db.Column(db.String(64), nullable=False)
    standard_drug_name = db.Column(db.String(64), nullable=False)
    dataset = db.Column(db.String(32), nullable=False)
    info = db.Column(db.Text)

    # This is a one-to-many relationship
    # exp can have many dosage/response
    dose_response = db.relationship('DoseResponse', backref='exp', lazy='dynamic')
    jags_sampling = db.relationship('JagsSampling', backref='exp', lazy='dynamic')
    sensitivity = db.relationship('Sensitive', backref='exp', lazy='dynamic')
    sensitivity_provided = db.relationship('SensitiveProvided', backref='exp', lazy='dynamic')
    drug_table = db.relationship('DrugTable', backref='exp', lazy='dynamic')
    cell_line_table = db.relationship('CellLineTable', backref='exp', lazy='dynamic')
    wildtype_mutation = db.relationship('WildtypeMutation', backref='exp', lazy='dynamic')
    gene_expression = db.relationship('GeneExpression', backref='exp', lazy='dynamic')


    def __init__(self, cellosaurus_index, cellosaurus_id, standard_drug_name, dataset, info):
        self.cellosaurus_index = cellosaurus_index
        self.cellosaurus_id = cellosaurus_id
        self.standard_drug_name = standard_drug_name
        self.dataset = dataset
        self.info = info


class DoseResponse(db.Model):
    __tablename__ = 'dose_response'

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
    __tablename__ = 'jags_sampling'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n_dosage = db.Column(db.Integer)
    min_dosage = db.Column(db.Float)
    max_dosage = db.Column(db.Float)
    beta0_mode = db.Column(db.Float)
    beta0_HDI_low = db.Column(db.Float)
    beta0_HDI_high = db.Column(db.Float)
    beta1_mode = db.Column(db.Float)
    # beta1_HDI_low = db.Column(db.Float)
    # beta1_HDI_high = db.Column(db.Float)
    # ic90_mode = db.Column(db.Float)
    # ic90_HDI_low = db.Column(db.Float)
    # ic90_HDI_high = db.Column(db.Float)
    # ec50_mode = db.Column(db.Float)
    # ec50_HDI_low = db.Column(db.Float)
    # ec50_HDI_high = db.Column(db.Float)
    # ecinf_mode = db.Column(db.Float)
    # ecinf_HDI_low = db.Column(db.Float)
    # ecinf_HDI_high = db.Column(db.Float)
    # auc_mode = db.Column(db.Float)
    # auc_HDI_low = db.Column(db.Float)
    # auc_HDI_high = db.Column(db.Float)
    beta0_jags_str = db.Column(db.Text)
    beta1_jags_str = db.Column(db.Text)

    # Connect the exp.
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)

    def __init__(self, n_dosage, min_dosage, max_dosage, beta0_mode, beta0_HDI_low, beta0_HDI_high, beta1_mode,
                 # beta1_HDI_low, beta1_HDI_high, ic90_mode, ic90_HDI_low, ic90_HDI_high,
                 # ec50_mode, ec50_HDI_low, ec50_HDI_high, ecinf_mode, ecinf_HDI_low, ecinf_HDI_high,
                 # auc_mode, auc_HDI_low, auc_HDI_high,
                 beta0_jags_str, beta1_jags_str, exp_id):
        self.n_dosage = n_dosage
        self.min_dosage = min_dosage
        self.max_dosage = max_dosage
        self.beta0_mode = beta0_mode
        self.beta0_HDI_low = beta0_HDI_low
        self.beta0_HDI_high = beta0_HDI_high
        self.beta1_mode = beta1_mode
        # self.beta1_HDI_low = beta1_HDI_low
        # self.beta1_HDI_high = beta1_HDI_high
        # self.ic90_mode = ic90_mode
        # self.ic90_HDI_low = ic90_HDI_low
        # self.ic90_HDI_high = ic90_HDI_high
        # self.ec50_mode = ec50_mode
        # self.ec50_HDI_low = ec50_HDI_low
        # self.ec50_HDI_high = ec50_HDI_high
        # self.ecinf_mode = ecinf_mode
        # self.ecinf_HDI_low = ecinf_HDI_low
        # self.ecinf_HDI_high = ecinf_HDI_high
        # self.auc_mode = auc_mode
        # self.auc_HDI_low = auc_HDI_low
        # self.auc_HDI_high = auc_HDI_high
        self.beta0_jags_str = beta0_jags_str
        self.beta1_jags_str = beta1_jags_str

        self.exp_id = exp_id


class Sensitive(db.Model):
    __tablename__ = 'sensitivity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ic50_HDI_low = db.Column(db.Float)
    ic50_HDI_high = db.Column(db.Float)
    ic50_mode = db.Column(db.Float)
    ic90_calculate = db.Column(db.Float)
    ec50_calculate = db.Column(db.Float)
    einf_calculate = db.Column(db.Float)
    auc_calculate = db.Column(db.Float)


    # Connect the exp.
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)

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


class SensitiveProvided(db.Model):
    __tablename__ = 'sensitivity_provided'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ic50_provided = db.Column(db.Float)
    auc_provided = db.Column(db.Float)

    # Connect the exp.
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)

    def __init__(self, ic50_provided, auc_provided, exp_id):
        self.ic50_provided = ic50_provided
        self.auc_provided = auc_provided

        self.exp_id = exp_id



class CellLineTable(db.Model):
    __tablename__ = 'cell_line_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ccle_name = db.Column(db.String(64))
    ctrp1_name = db.Column(db.String(64))
    ctrp2_name = db.Column(db.String(64))
    gdsc1_name = db.Column(db.String(64))
    gdsc2_name = db.Column(db.String(64))
    site = db.Column(db.String(64))
    # Connect the exp.
    cellosaurus_id = db.Column(db.String(64), db.ForeignKey('experiments.cellosaurus_id'), nullable=False)  #

    def __init__(self, site, cellosaurus_id, ccle_name, ctrp1_name, ctrp2_name, gdsc1_name, gdsc2_name):
        self.site = site
        self.ccle_name = ccle_name
        self.ctrp1_name = ctrp1_name
        self.ctrp2_name = ctrp2_name
        self.gdsc1_name = gdsc1_name
        self.gdsc2_name = gdsc2_name

        self.cellosaurus_id = cellosaurus_id


class DrugTable(db.Model):
    __tablename__ = 'drug_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    synonyms = db.Column(db.String(128))
    target = db.Column(db.String(64))
    pathway = db.Column(db.String(256))
    ccle_drug_name = db.Column(db.String(64))
    ctrp1_drug_name = db.Column(db.String(64))
    ctrp2_drug_name = db.Column(db.String(64))
    gdsc1_drug_name = db.Column(db.String(64))
    gdsc2_drug_name = db.Column(db.String(64))

    # Connect the exp.
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('experiments.standard_drug_name'), nullable=False)  #

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


class WildtypeMutation(db.Model):
    __tablename__ = 'wildtype_mutation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(64))
    dataset = db.Column(db.String(32))
    cancer_type = db.Column(db.String(64))
    pvalue = db.Column(db.Float)
    statistic = db.Column(db.Float)
    pvalue_provided = db.Column(db.Float)
    statistic_provided = db.Column(db.Float)

    # Connect the exp.
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('experiments.standard_drug_name'))  #

    def __init__(self, gene, dataset, cancer_type, pvalue, statistic, pvalue_provided, statistic_provided, standard_drug_name):
        self.gene = gene
        self.dataset = dataset
        self.cancer_type = cancer_type
        self.pvalue = pvalue
        self.statistic = statistic
        self.pvalue_provided = pvalue_provided
        self.statistic_provided = statistic_provided
        
        self.standard_drug_name = standard_drug_name

class GeneExpression(db.Model):
    __tablename__ = 'gene_expression'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gene = db.Column(db.String(64))
    dataset = db.Column(db.String(32))
    cancer_type = db.Column(db.String(64))
    pvalue = db.Column(db.Float)
    correlation = db.Column(db.Float)
    pvalue_provided = db.Column(db.Float)
    correlation_provided = db.Column(db.Float)

    # Connect the exp.
    standard_drug_name = db.Column(db.String(64), db.ForeignKey('experiments.standard_drug_name'))  #

    def __init__(self, gene, dataset, cancer_type, pvalue, correlation, pvalue_provided, correlation_provided, standard_drug_name):
        self.gene = gene
        self.dataset = dataset
        self.cancer_type = cancer_type
        self.pvalue = pvalue
        self.correlation = correlation
        self.pvalue_provided = pvalue_provided
        self.correlation_provided = correlation_provided

        self.standard_drug_name = standard_drug_name