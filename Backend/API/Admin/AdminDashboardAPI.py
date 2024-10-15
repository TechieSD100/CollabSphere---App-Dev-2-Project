# AdminDashboardAPI.py

from flask_restful import Resource
from models.models import Sponsor, Influencer, User
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from models.database import db
from Cache.CacheAPI import *


class AllInfluencersAPI(Resource):
    @jwt_required()
    def get(self):
        influencers = Influencer.query.all()

        influencerall = []

        for inf in influencers:
            user = User.query.filter_by(userid = inf.inf_id).first()

            influencer = {
                'inf_id': inf.inf_id,
                'username': user.username,  # Extract username from User
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach,
                'flag': inf.flag
            }
            influencerall.append(influencer)
        
        return {
            'status': 'success',
            'influencerdata': influencerall
        }, 200



class PendingSponsorAPI(Resource):
    @jwt_required()
    def get(self):
        sponsors = Sponsor.query.filter_by(budget=0).all()
        sponsors_data = [
            {
                'sponsor_id': sponsor.sponsor_id,
                'org_name': sponsor.org_name,
                'budget': sponsor.budget
            }
            for sponsor in sponsors
        ]

        return {
            'status': 'success',
            'sponsordata': sponsors_data
        }, 200



class DeclinedSponsorsListAPI(Resource):
    @jwt_required()
    def get(self):
        sponsors = Sponsor.query.filter_by(budget=2).all()
        dec_sponsors = [
            {
                'sponsor_id': sponsor.sponsor_id,
                'org_name': sponsor.org_name,
                'budget': sponsor.budget
            }
            for sponsor in sponsors
        ]

        return {
            'status': 'success',
            'dec_sponsors': dec_sponsors
        }, 200



class ApproveSponsorAPI(Resource):
    @jwt_required()
    def put(self, sponsor_id):
        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()

        if sponsor is None:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404

        sponsor.budget = 1
        db.session.commit()

        return {'status': 'success', 'message': f'Sponsor {sponsor.org_name} approved successfully'}, 200



class DeclineSponsorAPI(Resource):
    @jwt_required()  # Corrected decorator
    def put(self, sponsor_id):
        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()

        if sponsor is None:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404
        
        sponsor.budget = 2
        db.session.commit()

        return {'status': 'success', 'message': f'Sponsor {sponsor.org_name} was declined from signing up for the application.'}, 200



class ValidateSponsorAPI(Resource):
    @jwt_required()
    def put(self, sponsor_id):
        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()

        if sponsor is None:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404

        sponsor.budget = 0
        db.session.commit()

        return {'status': 'success', 'message': f'Sponsor {sponsor.org_name} moved to pending state successfully'}, 200
    



class FlagInfluencerAPI(Resource):
    @jwt_required()
    def put(self, inf_id):
        influencer = Influencer.query.filter_by(inf_id=inf_id).first()

        if influencer is None:
            return {'status': 'fail', 'message': 'Influencer not found'}, 404

        influencer.flag = 'flag'
        db.session.commit()

        return {'status': 'success', 'message': f'Influencer {influencer.inf_id} flagged successfully'}, 200


class UnflagInfluencerAPI(Resource):
    @jwt_required()
    def put(self, inf_id):
        influencer = Influencer.query.filter_by(inf_id=inf_id).first()

        if influencer is None:
            return {'status': 'fail', 'message': 'Influencer not found'}, 404

        influencer.flag = 'unflag'
        db.session.commit()

        return {'status': 'success', 'message': f'Influencer {influencer.inf_id} unflagged successfully'}, 200



