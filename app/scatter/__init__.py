from flask import Blueprint

scatter = Blueprint('scatter', __name__)

from . import views, errors
