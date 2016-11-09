from . import db

"""
Contains the sqlite tables and their attribute.
"""

class Bed(db.Model):
    __tablename__ = 'bed'
    file_location = db.Column(db.Text(64), primary_key=True)
    label = db.Column(db.String(64), unique=True)
    date = db.Column(db.Integer(), unique=True)
    user = db.Column(db.String(32), unique=False)
    md5 = db.Column(db.String(32), unique=True)

    def __init__(self, file_location, label, date, user, md5):
        self.file_location = file_location
        self.label = label
        self.date = date
        self.user = user
        self.md5 = md5

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'file_location' : self.file_location,
            'label'         : self.label,
            'date'          : self.date,
            'user'          : self.user,
            'md5'           : self.md5
        }

    def __repr__(self):
        return "'{0}', '{1}'".format(self.file_location, self.label)


class Colocalization(db.Model):
    __tablename__ = 'colocalization'
    file_location1 = db.Column(db.String(64), db.ForeignKey(
        'bed.file_location'), primary_key=True)
    file_location2 = db.Column(db.String(64), db.ForeignKey(
        'bed.file_location'), primary_key=True)
    method = db.Column(db.String(64), unique=False, primary_key=True)
    value = db.Column(db.Integer(), unique=False)

    def __init__(self, file_location1, file_location2, method, value):
        self.file_location1 = file_location1
        self.file_location2 = file_location2
        self.method = method
        self.value = value

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'file_location1' : self.file_location1,
            'file_location2' : self.file_location2,
            'method'         : self.method,
            'value'          : self.value
            }
    
    def __repr__(self):
        return "{0}, {1}, {2}, {3}".format(self.file_location1, self.file_location2, self.method, self.value)
