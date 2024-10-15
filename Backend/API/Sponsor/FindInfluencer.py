# InfluencerAPI.py

from flask_restful import Resource
from models.models import Influencer, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from flask import jsonify, request


class InfluencerSearchAPI(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        # Get the logged-in user's ID from the JWT token
        user_identity = get_jwt_identity()

        search_query = request.args.get('query', '').lower()

        #Fetch influencer details
        influencerall = []
        influencerusername = []
        influencercategory = []
        influencerniche = []

        influencers0  = Influencer.query.all()
        influencers1 = Influencer.query.filter(User.username.ilike(f"%{search_query}%")).all()
        influencers2 = Influencer.query.filter(Influencer.category.ilike(f"%{search_query}%")).all()
        influencers3 = Influencer.query.filter(Influencer.niche.ilike(f"%{search_query}%")).all()
        

        if search_query == "":
            influencers1 = []
            influencers2 = []
            influencers3 = []

        # Takes all influencers
        for inf in influencers0:
            user = User.query.filter_by(userid = inf.inf_id).first()
            # Prepare influencer data with username
            influencer = {
                'inf_id': inf.inf_id,
                'username': user.username,  # Extract username from User
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach
            }
            influencerall.append(influencer)

        
        # Takes influencer by username search
        for inf in influencers1:
            user = User.query.filter_by(userid = inf.inf_id).first()
            # Prepare influencer data with username
            influencer = {
                'inf_id': inf.inf_id,
                'username': user.username,  # Extract username from User
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach
            }
            influencerusername.append(influencer)


        # Takes influencer by category search
        for inf in influencers2:
            user = User.query.filter_by(userid = inf.inf_id).first()
            # Prepare influencer data with username
            influencer = {
                'inf_id': inf.inf_id,
                'username': user.username,  # Extract username from User
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach
            }
            influencercategory.append(influencer)


        # Takes influencer by niche search
        for inf in influencers3:
            user = User.query.filter_by(userid = inf.inf_id).first()
            # Prepare influencer data with username
            influencer = {
                'inf_id': inf.inf_id,
                'username': user.username,  # Extract username from User
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach
            }
            influencerniche.append(influencer)


        return jsonify({
            'status': 'success',
            'inf_all': influencerall,
            'inf_uname': influencerusername,
            'inf_cat': influencercategory,
            'inf_niche': influencerniche
        })