from flask.ext.wtf import Form
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField, SubmitField


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SelectFiles(Form):
    """
    Print out the checkbox values
    """
    files = MultiCheckboxField(u'Bed Files', coerce=int)
    submit = SubmitField('Submit')
