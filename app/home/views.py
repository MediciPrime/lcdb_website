from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import home


@home.route('/home', methods=['GET', 'POST'])
def base():
    return render_template('home/index.html',
                           name=session.get('name'),
                           known=session.get('known', False))
