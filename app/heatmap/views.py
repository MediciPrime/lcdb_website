from flask import render_template, redirect, url_for, request, session
from . import heatmap
from .forms import SelectFiles
from ..models import PBed
from .models import Heatmap


@heatmap.route('/heatmap', methods=['GET', 'POST'])
def base():
    select_files = SelectFiles()
    select_files.files.choices = [(f.id, f.name)
                                  for f in PBed.query.order_by('name')]
    jaccard_output = Heatmap(select_files.files.data)
    # print(jaccard_output.jaccard_output())
    session['files_selected'] = select_files.files.data
    if select_files.validate_on_submit():
        return redirect(url_for('.success'))
    return render_template('heatmap/index.html', form=select_files)


@heatmap.route('/heatmap/success', methods=['GET', 'POST'])
def success():
    return render_template('heatmap/success.html')
