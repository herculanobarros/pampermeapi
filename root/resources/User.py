from flask_restful import reqparse
from flask import request, json, Response, Blueprint, g
from root.models.User import User,UserSchema
from root.security.Authentication import Auth

# Initialize Parser
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('firstName', required=False)
parser.add_argument('lastName', required=False)
parser.add_argument('age', required=False)
parser.add_argument('phoneNumber', required=False)


user_api = Blueprint('users', __name__)
user_schema = UserSchema()


# CREATE USER
@user_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    user_in_db = User.find_by_username(data.get('username'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 400)

    # save user in DB
    user = User(data)
    user.save()

    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'accessToken': token}, 200)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


# GET SPECIFIC USER
@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_user_required
def get_a_user(user_id):
    user = User.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


# GET ALL USERS
@user_api.route('/all', methods=['GET'])
def get_all():
    users = User.get_all_users()
    ser_users = user_schema.dump(users, many=True).data
    return custom_response({"data": ser_users}, 200)


# USER LOGIN
@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('username') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    user_in_db = User.find_by_username(data.get('username'))

    if not user_in_db:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not user_in_db.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = user_schema.dump(user_in_db).data

    token = Auth.generate_token(ser_data.get('username'))

    return custom_response({'jwt_token': token}, 200)


@user_api.route('/update', methods=['PUT'])
@Auth.auth_user_required
def update():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    user = User.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/account', methods=['DELETE'])
@Auth.auth_user_required
def delete():
    user = User.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 20)
