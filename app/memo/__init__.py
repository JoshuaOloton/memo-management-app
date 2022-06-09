from flask import Blueprint

memo = Blueprint("memo", __name__)

from . import views