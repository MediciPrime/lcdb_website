from flask import render_template
from . import home


@home.route('/', methods=['GET'])
def base():
    return render_template('home/index.html')
