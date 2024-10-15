# SponsorCampaignsAPI.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Sponsor, Campaign, AdRequest
from flask import jsonify
from models.database import db  # Ensure you import the database instance
from flask import abort
from Cache.CacheAPI import *

class CampaignsAPI(Resource):
    @jwt_required()  # Ensure the sponsor is logged in
    def get(self):
        # Existing GET method to fetch campaigns
        user_identity = get_jwt_identity()

        sponsor = Sponsor.query.filter_by(userid=user_identity['user_id']).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404

        campaigns = get_all_campaigns(sponsor.sponsor_id)

        campaigns_data = [
            {
                'camp_id': campaign.camp_id,
                'camp_name': campaign.camp_name,
                'camp_description': campaign.camp_description,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals
            } for campaign in campaigns
        ]

        return jsonify({
            'status': 'success',
            'data': campaigns_data
        })

from flask import abort

class CampaignDetailAPI(Resource):
    @jwt_required()
    def delete(self, camp_id):
        # Get the logged-in user's ID
        user_identity = get_jwt_identity()
        
        # Query the sponsor based on the logged-in user ID
        sponsor = Sponsor.query.filter_by(userid=user_identity['user_id']).first()
        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404
        
        # Find the campaign
        campaign = Campaign.query.filter_by(camp_id=camp_id, sponsor_id=sponsor.sponsor_id).first()
        if not campaign:
            return {'status': 'fail', 'message': 'Campaign not found'}, 404
        
        # Delete associated ad requests
        AdRequest.query.filter_by(camp_id=camp_id).delete()

        # Delete the campaign
        db.session.delete(campaign)
        db.session.commit()

        return {'status': 'success', 'message': 'Campaign deleted successfully'}, 200
