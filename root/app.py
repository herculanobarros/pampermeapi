from flask import Flask
from flask_jwt_extended import JWTManager
from root.commands import create_tables
from root.extensions import db, login_manager
from root.resources import User
from root.models import RevokedTokenModel
from flask_restful import Api
from flask_bcrypt import Bcrypt

app = Flask(__name__)
jwt = JWTManager(app)
bcrypt = Bcrypt()


def create_app(config_file='settings.py'):
    api = Api(app)
    app.config.from_pyfile(config_file)

    # Setup JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'JWT_Pamper_me'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    # API Endpoints(Resources)
    api.add_resource(User.UserRegistration, '/registration')
    api.add_resource(User.UserLogin, '/login')
    api.add_resource(User.UserLogoutAccess, '/logout/access')
    api.add_resource(User.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(User.TokenRefresh, '/token/refresh')
    api.add_resource(User.AllUsers, '/users')
    api.add_resource(User.SecretResource, '/secret')

    app.cli.add_command(create_tables)

    return app


@app.route('/')
def index():
    return 'it works!'


# this method is called every single time client make secure request
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.RevokedTokenModel.is_jti_blacklisted(jti)
