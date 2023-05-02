from flask import (
    Blueprint, jsonify, g, redirect, request, url_for
)

from app.db import db_data_teams

bp = Blueprint('teams', __name__, url_prefix='/api/team')

# /api/team/
@bp.route('/')
def return_all():
    return jsonify(db_data_teams())

# /api/team/banana
@bp.route('/<string:name>')
def return_one(name):
    return jsonify(db_data_teams()[f'{name}'])

# /api/team/banana/tasks
@bp.route('/<string:name>/<string:value>')
def return_tasks(name, value):
    return jsonify(db_data_teams()[f"{name}"][f"{value}"])

