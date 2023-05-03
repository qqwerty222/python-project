from flask import (
    Blueprint, jsonify, g, redirect, render_template, request, url_for
)

from app.db import db_data_company
from app.db import db_data_teams
from app.db import db_data_workers

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    company = db_data_company()
    teams   = db_data_teams()
    workers = db_data_workers()

    return render_template('index.html', company=company, teams=teams, workers=workers)
    