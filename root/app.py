from flask import Flask
from root.extensions import db
from root.resources.Babysitter import babysitter_api
from root.resources.User import user_api

app = Flask(__name__)

def create_app():
    db.init_app(app)

    app.register_blueprint(user_api, url_prefix='/api/v1/users')
    app.register_blueprint(babysitter_api, url_prefix='/api/v1/babysitters')

    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET'])
    def index():
        return 'Congratulations!'

    return app
