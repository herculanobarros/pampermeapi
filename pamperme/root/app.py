from flask import Flask
from pamperme.root.models import db
from pamperme.root.resources import User
from pamperme.root.resources import Babysitter
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run()

# def create_app():
#     db.init_app(app)
#
#     app.register_blueprint(user_api, url_prefix='/api/v1/users')
#     app.register_blueprint(babysitter_api, url_prefix='/api/v1/babysitters')
#
#     with app.app_context():
#         db.create_all()
#
#     @app.route('/', methods=['GET'])
#     def index():
#         return 'Congratulations!'
#
#     return app
