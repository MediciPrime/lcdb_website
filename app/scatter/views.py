from flask import render_template, redirect, url_for, request, session
from flask.json import dumps
from flask.ext.login import current_user
from . import scatter
from .forms import SelectFiles
from ..models import RNAseq
from .models import Scatter


@scatter.route('/', methods=['GET', 'POST'])
def base():

    # create 'select_files' object from 'SelectFiles' class
    select_files = SelectFiles()

    # order the selection process to display only desired files
    select_files.pfiles.choices = [(f.file_location, f.label)
                                   for f in RNAseq.query.filter_by(user='public')]

    # display user data if logged in and confirmed
    if current_user.is_authenticated \
       and current_user.confirmed:
        select_files.ufiles.choices = [(f.file_location, f.label)
                                      for f in RNAseq.query.filter_by(user=getattr(current_user, "username"))]
    else:
        select_files.ufiles.choices = []

    # process that occurs after file is selected and form is submitted
    if select_files.validate_on_submit():
        session['files_selected'] = select_files.pfiles.data + select_files.ufiles.data
        session['adjpval'] = select_files.adjpval.data

        # create 'maplot_output' object
        maplot_output = Scatter(
            session['files_selected'], session['adjpval'])

        # obtain maplot output
        output = maplot_output.get_dictionary()

        print(output[0])
        
        # dump data and set to maplotJson
        maplotJson = dumps({'baseMean' : output[0], 'log2FoldChange': output[1], 'name' : output[2]}, )
        
        # with session cookie set redirect to success
        return render_template('scatter/success.html', maplotData=maplotJson)
    return render_template('scatter/index.html', form=select_files)


@scatter.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('scatter/success.html')
