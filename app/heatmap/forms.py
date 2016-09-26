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
    staticmethods = [
        'Jaccard\r\nFisher-Exact\r\nGAT_Log-Fold\r\nGAT_Percent_Overlay\r\nInterval_Stats']
    list_stat = staticmethods[0].split()
    smethods = [(x, x) for x in list_stat]
    methods = MultiCheckboxField(u'Statistics', choices=smethods)
    submit = SubmitField('Submit')
