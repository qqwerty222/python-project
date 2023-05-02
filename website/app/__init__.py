from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    # test page
    @app.route('/test')
    def test():
        return 'test page'

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    return app
