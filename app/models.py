from . import db

"""
Contains the sqlite tables and their attribute.
"""

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Bed(db.Model):
    __tablename__ = 'beds'
    file_location = db.Column(db.Text(64), unique=True)
    label = db.Column(db.String(64), unique=True)
    date = db.Column(db.Integer(), unique=False)
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
    __tablename__ = 'identities'
    organism = db.Column(db.String(32), unique=False)
    technique = db.Column(db.String(32), unique=False)
    afactor = db.Column(db.String(32), unique=False)
    tissue = db.Column(db.String(32), unique=False)
    cline = db.Column(db.String(32), unique=False)
    wld = db.Column(db.String(32), unique=False)
    dld = db.Column(db.String(32), unique=False)
    md5 = db.Column(db.String(32), db.ForeignKey('beds.md5'), primary_key=True)

    def __init__(self, organism, technique, afactor, tissue, cline, wld, dld, md5):
        self.organism = organism,
        self.technique = technique,
        self.afactor = afactor,
        self.tissue = tissue,
        self.cline = cline,
        self.wld = wld,
        self.dld = dld,
        self.md5 = md5

    def __repr__(self):
        return "'{0}', '{1}'".format(self.organism, self.md5)

class Colocalization(db.Model):
    __tablename__ = 'colocalizations'
    method = db.Column(db.String(64), unique=False, primary_key=True)
    value = db.Column(db.Integer(), unique=False)
    md5_1 = db.Column(db.String(32), db.ForeignKey('beds.md5'), primary_key=True)
    md5_2 = db.Column(db.String(32), db.ForeignKey('beds.md5'), primary_key=True)

    def __init__(self, method, value, md5_1, md5_2):
        self.method = method
        self.value = value
        self.md5_1 = md5_1
        self.md5_2 = md5_2
    
    def __repr__(self):
        return "{0}, {1}, {2}, {3}".format(self.md5_1, self.md5_2, self.method, self.value)
