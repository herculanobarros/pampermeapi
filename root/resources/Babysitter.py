from flask import request, json, Response, Blueprint, g
from root.models.Babysitter import Babysitter, BabysitterSchema
from root.security.Authentication import Auth

babysitter_api = Blueprint('babysitters', __name__)
babysitter_schema = BabysitterSchema()


# GET SPECIFIC BABYSITTER
@babysitter_api.route('/<int:babysitter_id>', methods=['GET'])
@Auth.auth_babysitter_required
def get_a_babysitter(babysitter_id):
    babysitter = Babysitter.get_one_babysitter(babysitter_id)
    if not babysitter:
        return custom_response({'error': 'user not found'}, 404)

    ser_babysitter = babysitter_schema.dump(babysitter).data
    return custom_response(ser_babysitter, 200)


# GET ALL BABYSITTERS
@babysitter_api.route('/all', methods=['GET'])
def get_all():
    babysitters = Babysitter.get_all_babysitters()
    ser_babysitters = babysitter_schema.dump(babysitters, many=True).data
    return custom_response({"data" : ser_babysitters}, 200)


# LOGIN BABYSITTER
@babysitter_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    data, error = babysitter_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('username') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    babysitter = Babysitter.find_by_username(data.get('username'))

    if not babysitter:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not babysitter.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = babysitter_schema.dump(babysitter).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'accessToken': token}, 200)


# CREATE
@babysitter_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = babysitter_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    babysitter_in_db = Babysitter.find_by_username(data.get('username'))
    if babysitter_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 400)

    # save babysitter in DB
    babysitter = Babysitter(data)
    babysitter.save()

    babysitter_data = babysitter_schema.dump(babysitter).data
    token = Auth.generate_token(babysitter_data.get('id'))

    return custom_response({'accessToken': token}, 200)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


# DELETE ACCOUNT
@babysitter_api.route('/delete', methods=['DELETE'])
@Auth.auth_babysitter_required
def delete():
    babysitter = Babysitter.get_one_babysitter(g.babysitter.get('id'))
    babysitter.delete()
    return custom_response({'message': 'deleted'}, 200)


@babysitter_api.route('/update', methods=['PUT'])
@Auth.auth_babysitter_required
def update():
    req_data = request.get_json()
    data, error = babysitter_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    babysitter = Babysitter.get_one_user(g.babysitter.get('id'))
    babysitter.update(data)
    ser_babysitter = babysitter_schema.dump(babysitter).data
    return custom_response(ser_babysitter, 200)