from . import db


class PBed(db.Model):
    __tablename__ = 'public_bed'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    file_location = db.Column(db.String(64), unique=True)

    def __init__(self, name, file_location):
        self.name = name
        self.file_location = file_location

    def __repr__(self):
        return '%r' % self.name


class Jaccard(db.Model):
    __tablename__ = 'jaccard'
    p_id = db.Column(db.Integer, db.ForeignKey(
        'public_bed.id'), primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    file_location = db.Column(db.String(64), unique=True)
    pbed = db.relationship('PBed', backref='pbed')

    def __init__(self, name, file_location):
        self.name = name
        self.file_location = file_location

    def __repr__(self):
        return '<Jaccard %r>' % self.file_location
