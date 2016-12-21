from flask.ext.wtf import Form
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField, SubmitField, RadioField


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SelectFiles(Form):

    # display public files
    pfiles = SelectMultipleField(u'Public Bed Files', coerce=str)  # print out checkbox values
    
    # display user specific files
    ufiles = SelectMultipleField(u'User Bed Files', coerce=str)

    # print out radio values
    list_stat = ['Jaccard', 'Fisher Exact', 'GAT Log Fold', 'GAT Percent Overlay', 'Interval Stats']
    smethods = [(x, x) for x in list_stat]
    methods = RadioField(u'Statistics', choices=smethods)

    # print submit field
    submit = SubmitField('Submit')
