from functools import wraps
import jwt
from flask import json, Response, request, g
from root.models.Babysitter import Babysitter
from root.models import User


class Auth:
    @staticmethod
    def generate_token(username):
        return jwt.encode({'data': str(username)}, 'secret', algorithm='HS256').decode("utf-8")

    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, "JWT_KEY", algorithms='RS256')
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    @staticmethod
    def auth_user_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = User.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth

    # babysitter decorator
    @staticmethod
    def auth_babysitter_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            babysitter_id = data['data']['babysitter_id']
            check_user = Babysitter.get_one_babysitter(babysitter_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.babysitter = {'id': babysitter_id}
            return func(*args, **kwargs)

        return decorated_auth