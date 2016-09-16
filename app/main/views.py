from flask import render_template
from . import main
from .forms import SelectFiles
from ..models import PBed


def populate_form(select_files):
    """
    Pulls choices from database to populate select fields
    """
    string_of_files = PBed.query.all()
    tuple_of_files = tuple(string_of_files)
    files = [(x, x) for x in tuple_of_files]
    select_files.example.choices = files


@main.route('/', methods=['GET', 'POST'])
def index():
    select_files = SelectFiles()
    populate_form(select_files)
    print(select_files.example.data)
    return render_template('index.html', form=select_files)
