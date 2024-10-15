# SignupAPI.py

import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from flask_security.utils import hash_password
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask import Flask, request, jsonify
def method_name():
    pass
from config.validation import  BusinessValidationError

from models.models import  User , Influencer , Sponsor
from models.database import db


class SignupInfluencerAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')

        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        influencer = Influencer(
            username=username,
            password=hash_password(password),
            role='influencer',
            category=category,
            niche=niche,
            reach=reach,
            flag="unflag"
        )
        
        db.session.add(influencer)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Signup successful! You can now log in.'})

class SignupSponsorAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        org_name = data.get('org_name')

        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        sponsor = Sponsor(
            username=username,
            password=hash_password(password),
            role='sponsor',
            org_name=org_name,
            budget = 0
        )
        
        db.session.add(sponsor)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Signup successful! You can now log in.'})
