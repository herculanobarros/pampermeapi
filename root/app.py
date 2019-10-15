from flask import Flask
from root.models import db
from root.resources import Babysitter
from root.resources import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:pampermedb@localhost:5432/pampermedb"


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
