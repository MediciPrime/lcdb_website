from flask import Blueprint

heatmap = Blueprint('heatmap', __name__, template_folder="templates")

from . import views, errors
