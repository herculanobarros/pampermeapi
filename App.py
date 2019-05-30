from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from main.resources import User
from main.models import RevokedTokenModel, Appointment

app = Flask(__name__)
app.secret_key = 'pamper_me'
api = Api(app)
db = SQLAlchemy(app)
db.create_all()

#setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'pamper_me'


#Setup JWT Configuration
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
api.add_resource(Appointment.CreateAppointment,'/create/appointment')

# Run Server
if __name__ == '__main__':
    from main.db import db
    db.init_app(app)
    app.run(debug=True)
