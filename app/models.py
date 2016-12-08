from . import db

"""
Contains the sqlite tables and their attribute.
"""

class Bed(db.Model):
    __tablename__ = 'bed'
    file_location = db.Column(db.Text(64), unique=True)
    label = db.Column(db.String(64), unique=True)
    date = db.Column(db.Integer(), unique=True)
    user = db.Column(db.String(32), unique=False)
    md5 = db.Column(db.String(32), primary_key=True)

    def __init__(self, file_location, label, date, user, md5):
        self.file_location = file_location
        self.label = label
        self.date = date
        self.user = user
        self.md5 = md5

    def __repr__(self):
        return "'{0}', '{1}', '{2}'".format(self.file_location, self.label, self.md5)

class Identity(db.Model):
    __tablename__ = 'identity'
    organism = db.Column(db.String(32), unique=False)
    technique = db.Column(db.String(32), unique=False)
    afactor = db.Column(db.String(32), unique=False)
    tissue = db.Column(db.String(32), unique=False)
    cline = db.Column(db.String(32), unique=False)
    md5 = db.Column(db.String(32), db.ForeignKey('bed.md5'), primary_key=True)

    def __init__(self, organism, technique, afactor, tissue, cline, md5):
        self.organism = organism,
        self.technique = technique,
        self.afactor = afactor,
        self.tissue = tissue,
        self.cline = cline,
        self.md5 = md5

    def __repr__(self):
        return "'{0}', '{1}'".format(self.organism, self.md5)

class Colocalization(db.Model):
    __tablename__ = 'colocalization'
    method = db.Column(db.String(64), unique=False, primary_key=True)
    value = db.Column(db.Integer(), unique=False)
    md5_1 = db.Column(db.String(32), db.ForeignKey('bed.md5'), primary_key=True)
    md5_2 = db.Column(db.String(32), db.ForeignKey('bed.md5'), primary_key=True)

    def __init__(self, method, value, md5_1, md5_2):
        self.method = method
        self.value = value
        self.md5_1 = md5_1
        self.md5_2 = md5_2
    
    def __repr__(self):
        return "{0}, {1}, {2}, {3}".format(self.md5_1, self.md5_2, self.method, self.value)
