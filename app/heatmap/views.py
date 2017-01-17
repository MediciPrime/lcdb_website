from flask import render_template, redirect, url_for, request, session
from flask.json import dumps
from flask.ext.login import current_user
from . import heatmap
from .forms import SelectFiles
from ..models import Bed
from .models import Heatmap


@heatmap.route('/', methods=['GET', 'POST'])
def base():

    # create 'select_files' object from 'SelectFiles' class
    select_files = SelectFiles()

    # order the selection process to display only desired files
    select_files.pfiles.choices = [(f.file_location, f.label)
                                   for f in Bed.query.filter_by(user='public')]

    # display user data if logged in and confirmed
    if current_user.is_authenticated \
       and current_user.confirmed:
        select_files.ufiles.choices = [(f.file_location, f.label)
                                      for f in Bed.query.filter_by(user=getattr(current_user, "username"))]
    else:
        select_files.ufiles.choices = []

    # process that occurs after file is selected and form is submitted
    if select_files.validate_on_submit():
        session['files_selected'] = select_files.pfiles.data + select_files.ufiles.data
        session['stat_method'] = select_files.methods.data

        # create 'colocalization_output' object
        colocalization_output = Heatmap(
            session['files_selected'], select_files.methods.data)

        # determine_method selected by user and generate answer
        output = colocalization_output.determine_method()

        # dump data and set to heatmapJson
        heatmapJson = dumps({'nodes' : output[0], 'links': output[1]})
        
        # with session cookie set redirect to success
        return render_template('heatmap/success.html', heatmapData=heatmapJson)
    return render_template('heatmap/index.html', form=select_files)


@heatmap.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('heatmap/success.html')
