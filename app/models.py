from . import db


class PBed(db.Model):
    __tablename__ = 'public_bed'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    file_location = db.Column(db.String(64), unique=True)

    def __init__(self, name, file_location):
        self.name = name
        self.file_location = file_location

    def __repr__(self):
        return "'{0}', '{1}'".format(self.name, self.file_location)


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
        return "'{0}', '{1}', '{2}'".format(self.name,
                                            self.file_location,
                                            self.pbed)
