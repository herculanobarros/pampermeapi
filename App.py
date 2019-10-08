from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager
from flask_restful import Api
import Config
from models import RevokedTokenModel
from resources import User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'pamper_me'
api = Api(app)

Base = declarative_base()

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

#Session
session = Session()

# Setup JWT Configuration
app.config['JWT_SECRET_KEY'] = 'JWT_Pamper_me'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)


# this method is called every single time client make secure request
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.RevokedTokenModel.is_jti_blacklisted(jti)


# API Endpoints(Resources)
api.add_resource(User.UserRegistration, '/registration')
api.add_resource(User.UserLogin, '/login')
api.add_resource(User.UserLogoutAccess, '/logout/access')
api.add_resource(User.UserLogoutRefresh, '/logout/refresh')
api.add_resource(User.TokenRefresh, '/token/refresh')
api.add_resource(User.AllUsers, '/users')
api.add_resource(User.SecretResource, '/secret')

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
