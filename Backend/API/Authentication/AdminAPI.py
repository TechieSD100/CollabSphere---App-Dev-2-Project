import jwt
from functools import wraps
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import User
from models.database import db
from config.security import user_datastore
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security.utils import hash_password

admin_parser = reqparse.RequestParser()
admin_parser.add_argument('username')
admin_parser.add_argument('password')

class AdminLoginAPI(Resource):
    def post(self):
        args = admin_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.role == 'admin'  :
                if verify_password(password, user.password):
                    access_token = create_access_token(identity=user.userid, expires_delta=timedelta(seconds=1200))
                    login_user(user)
                else:
                    raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Incorrect password!")
            else:
                raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Only admin access allowed!")
        else:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="User not found!")
        return jsonify({'status': 'success','message': 'loggin Successfull !!', 'access_token': access_token, "username": username , 'role' : user.role})
	

class SignupAdminAPI(Resource):
    def post(self):
        args = admin_parser.parse_args()
        username = args.get('username')
        password = args.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400
        
        new_user = User(
            username=username, 
            password = hash_password(password),
            role = 'admin',
            )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Signup successful! You can now log in.'})


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  

        user_id = get_jwt_identity()  
        user = User.query.get(user_id) 

        if not user :
            response = jsonify(message="User required")
            response.status_code = 403
            return response

        return func(*args, **kwargs)

    return decorated_function