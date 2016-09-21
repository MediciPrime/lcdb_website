from flask import render_template, redirect, url_for, request
from . import heatmap
from .forms import SelectFiles
from ..models import PBed


@heatmap.route('/heatmap', methods=['GET', 'POST'])
def base():
    select_files = SelectFiles()
    select_files.files.choices = [(f.id, f.name)
                                  for f in PBed.query.order_by('name')]
    print(select_files.files.data)
    data = select_files.files.data
    if select_files.validate_on_submit():
        return redirect(url_for('heatmap.success', data=data))
    return render_template('heatmap/index.html', form=select_files)


@heatmap.route('/heatmap/success', methods=['GET'])
def success():
    return render_template('heatmap/success.html')
