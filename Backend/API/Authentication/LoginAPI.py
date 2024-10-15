# LoginAPI.py

import jwt
from functools import wraps
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import User, Sponsor, Influencer
from models.database import db
from config.security import user_datastore
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')

class LoginAPI(Resource):
    def post(self):
        args = user_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user.role != 'admin':
                if verify_password(password, user.password):
                    access_token = create_access_token(identity={'user_id': user.userid, 'role': user.role}, expires_delta=timedelta(seconds=1200))
                    login_user(user)

                    # Fetch additional info based on role
                    if user.role == 'sponsor':
                        sponsor = Sponsor.query.filter_by(userid=user.userid).first()
                        response = {
                            'status': 'success',
                            'message': 'Login successful!',
                            'access_token': access_token,
                            'role': user.role,
                            'username': username,
                            'sponsor_id': sponsor.sponsor_id
                        }
                    elif user.role == 'influencer':
                        influencer = Influencer.query.filter_by(userid=user.userid).first()
                        response = {
                            'status': 'success',
                            'message': 'Login successful!',
                            'access_token': access_token,
                            'role': user.role,
                            'username': username,
                            'inf_id': influencer.inf_id
                        }
                    else:
                        response = {
                            'status': 'success',
                            'message': 'Login successful!',
                            'access_token': access_token,
                            'role': user.role,
                            'username': username
                        }
                    
                    return jsonify(response)
                else:
                    raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Incorrect password!")
            else:
                raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Only users are allowed!")
        else:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="User not found!")


def user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Verify JWT token in the request

        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        user = User.query.get(user_id)  # Fetch the user object from the database

        if not user or user.role == 'admin':
            return jsonify(message="User required"), 403

        return func(*args, **kwargs)

    return decorated_function
