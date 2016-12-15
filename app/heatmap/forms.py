from flask.ext.wtf import Form
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField, SubmitField, RadioField


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SelectFiles(Form):

    files = SelectMultipleField(u'Bed Files', coerce=str)  # print out checkbox values

    # print out radio values
    list_stat = ['Jaccard', 'Fisher Exact', 'GAT Log Fold', 'GAT Percent Overlay', 'Interval Stats']
    smethods = [(x, x) for x in list_stat]
    methods = RadioField(u'Statistics', choices=smethods)

    # print submit field
    submit = SubmitField('Submit')
