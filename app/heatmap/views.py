from flask import render_template, redirect, url_for, request, session
from . import heatmap
from .forms import SelectFiles
from ..models import Bed
from .models import Heatmap


@heatmap.route('/heatmap', methods=['GET', 'POST'])
def base():
    select_files = SelectFiles()
    select_files.files.choices = [(f.file_location, f.label)
                                  for f in Bed.query.order_by('label')]
    if select_files.validate_on_submit():
        session['files_selected'] = select_files.files.data
        session['stat_method'] = select_files.methods.data
        colocalization_output = Heatmap.determine_method(
            select_files.files.data, select_files.methods.data)
        # colocalization_output.jaccard_output()
        return redirect(url_for('.success'))
    return render_template('heatmap/index.html', form=select_files)


@heatmap.route('/heatmap/success', methods=['GET', 'POST'])
def success():
    return render_template('heatmap/success.html')
