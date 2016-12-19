from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('Welcome to LCDB Website!  Please Login.', validators=[Required()])
    submit = SubmitField('Submit')
