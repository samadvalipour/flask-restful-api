from flask import Blueprint

site = Blueprint("site", __name__, url_prefix="/site/")
from . import views
