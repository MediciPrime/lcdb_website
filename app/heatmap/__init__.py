from flask import Blueprint

heatmap = Blueprint('heatmap', __name__)

from . import views, errors
