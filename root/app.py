from flask import Flask
from root.models import db
from root.resources import User
from root.resources import Babysitter
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


def create_app():
    db.init_app(app)
    app.register_blueprint(User.user_api, url_prefix='/api/v1/users')
    app.register_blueprint(Babysitter.babysitter_api, url_prefix='/api/v1/babysitters')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app()
    app.run()
