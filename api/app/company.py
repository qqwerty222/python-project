from flask import (
    Blueprint, jsonify, g, redirect, request, url_for
)

from app.db import db_data_company

bp = Blueprint('company', __name__, url_prefix='/api/company')

# /api/company/
@bp.route('/')
def return_all():
    return jsonify(db_data_company())



