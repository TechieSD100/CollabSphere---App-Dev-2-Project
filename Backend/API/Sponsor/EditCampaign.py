from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Sponsor, Campaign
from flask import jsonify, request
from models.database import db
from datetime import date

class EditCampaignsAPI(Resource):
    @jwt_required()
    def get(self, camp_id):
        user_identity = get_jwt_identity()
        sponsor = Sponsor.query.filter_by(userid=user_identity['user_id']).first()
        
        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404
        
        campaign = Campaign.query.filter_by(camp_id=camp_id, sponsor_id=sponsor.sponsor_id).first()
        
        if not campaign:
            return {'status': 'fail', 'message': 'Campaign not found'}, 404
        
        return {
            'status': 'success',
            'data': {
                'camp_id': campaign.camp_id,
                'camp_name': campaign.camp_name,
                'camp_description': campaign.camp_description,
                'start_date': campaign.start_date.isoformat(),  # Convert to string
                'end_date': campaign.end_date.isoformat(),      # Convert to string
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
            }
        }, 200

    @jwt_required()
    def put(self, camp_id):
        user_identity = get_jwt_identity()
        sponsor = Sponsor.query.filter_by(userid=user_identity['user_id']).first()
        
        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404
        
        campaign = Campaign.query.filter_by(camp_id=camp_id, sponsor_id=sponsor.sponsor_id).first()
        
        if not campaign:
            return {'status': 'fail', 'message': 'Campaign not found'}, 404
        
        data = request.get_json()

        campaign.camp_name = data['camp_name']
        campaign.camp_description = data['camp_description']
        campaign.start_date = date.fromisoformat(data['start_date'])  # Assuming you pass date as string
        campaign.end_date = date.fromisoformat(data['end_date'])      # Assuming you pass date as string
        campaign.budget = data['budget']
        campaign.visibility = data['visibility']
        campaign.goals = data['goals']

        db.session.commit()
        return {'status': 'success', 'message': 'Campaign updated successfully'}, 200
