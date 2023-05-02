from flask import Flask
from flask import jsonify

def create_app():
    # create and configure the app
    app = Flask(__name__)

    @app.route('/api')
    def all_data():
        return 'there will be all data'

    @app.route('/api/status')
    def welcome():
        return "Ok!"

    from . import workers
    app.register_blueprint(workers.bp)

    from . import teams
    app.register_blueprint(teams.bp)

    from . import company
    app.register_blueprint(company.bp)

    return app
