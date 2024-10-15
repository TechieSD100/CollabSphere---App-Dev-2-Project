# app.py

from flask import request, jsonify
from flask_restful import Resource
from models.models import db, Campaign
from datetime import datetime

class AddCampaignAPI(Resource):
    def post(self):
        data = request.get_json()
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError as e:
            return jsonify({'status': 'error', 'message': f'Invalid date format: {e}'}), 400
    
        campaign = Campaign(
        camp_name=data['camp_name'],
        camp_description=data['camp_description'],
        start_date=start_date,
        end_date=end_date,
        budget=data['budget'],
        visibility=data['visibility'],
        goals=data['goals'],
        sponsor_id=data['sponsor_id']
        )

        db.session.add(campaign)
        db.session.commit()
    
        return jsonify({'status': 'success', 'message': 'Campaign added successfully'})