from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from root.models import Babysitter
from root.models import RevokedTokenModel
from root.models import User

from root.resources import User

# Initialize Parser
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('firstName', required=False)
parser.add_argument('lastName', required=False)
parser.add_argument('age', required=False)
parser.add_argument('phoneNumber', required=False)


class UserRegistration(Resource):
    def post(self):
        parser.add_argument('isBabysitter', help='This field cannot be blank', required=True)

        data = parser.parse_args()
        is_babysitter = data.get('isBabysitter')

        if not is_babysitter:
            parser.add_argument('hourPrice', required=False)
            if Babysitter.find_by_username(data['username']):
                return {'message': 'User {} already exists'.format(data['username'])}

            newBabysitter = Babysitter(
                username=data['username'],
                password=User.generate_hash(data['password']),
                first_name=data['firstName'],
                last_name=data['lastName'],
                age=data['age'],
                region=data['region'],
                hour_price=data['hourPrice'],
                phone_number=data['phoneNumber'],
            )
            try:
                newBabysitter.save_to_db()
                # Create AcessToken and RefreshToken
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {
                    'message': 'User {} was created'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            except exc.SQLAlchemyError:
                self.logger.error(f"{self.name}: error during event write", exc_info=1)
        else:

            if User.find_by_username(data['username']):
                return {'message': 'User {} already exists'.format(data['username'])}

            new_user = User(
                username=data['username'],
                password=User.generate_hash(data['password']),
                first_name=data['firstName'],
                last_name=data['lastName'],
                age=data['age'],
                phone_number=data['phoneNumber']
            )
            try:
                new_user.save_to_db()
                # Create AcessToken and RefreshToken
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {
                    'message': 'User {} was created'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            except exc.SQLAlchemyError:
                self.logger.error(f"{self.name}: error during event write", exc_info=1)


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        # check if user exist if not give the error message
        currentUser = User.find_by_username(data['username'])

        if not currentUser:
            return {'message': 'user {} not exists on database'.format(data['username'])}

        if User.verify_hash(data['password'], currentUser.password) == currentUser.password:

            # Create acess_token and refreshToken
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(currentUser.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong crentials. Try again please'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return User.showAllUsers()

    def delete(self):
        return User.deleteAllUsers()


class AllBabysitters(Resource):
    def get(self):
        return Babysitter.showAllBabysitters()

    def delete(self):
        return Babysitter.deleteAllBabysitters()


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
