from flask.ext.wtf import Form
from wtforms.fields import SelectMultipleField, SubmitField, DecimalField


class SelectFiles(Form):

    # display public files
    pfiles = SelectMultipleField(u'Public RNA-Seq Files', coerce=str)  # print out checkbox values
    
    # display user specific files
    ufiles = SelectMultipleField(u'User RNA-Seq Files', coerce=str)

    # Allow adjusted p-values to be inserted
    adjpval = DecimalField(u'Adjusted p-value')

    # print submit field
    submit = SubmitField('Submit')
