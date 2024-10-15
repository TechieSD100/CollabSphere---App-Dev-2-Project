# CreateAd.py
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Influencer, User, AdRequest, Campaign
from flask import jsonify, request
from flask_cors import cross_origin
from models.database import db

class FetchInfluencerAPI(Resource):
  @jwt_required()
  @cross_origin()
  def get(self):
    # Get the logged-in user's ID from the JWT token
    user_identity = get_jwt_identity()

    # Fetch influencer details
    influencerdata = []
    influencers = Influencer.query.all()
    for inf in influencers:
        user = User.query.filter_by(userid = inf.inf_id).first()

    # Prepare influencer data with username
        influencer = {
            'inf_id': inf.inf_id,
            'username': user.username,  # Extract username from User
            'category': inf.category,
            'niche': inf.niche,
            'reach': inf.reach
        }

        influencerdata.append(influencer)
    
    return jsonify({
       'status': 'success',
       'inf_data': influencerdata
    })
  


class CreateAdAPI(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        # Extract data from the request
        data = request.get_json()
        sponsor_id = data.get('sponsor_id')
        camp_id = data.get('camp_id')
        inf_id = data.get('inf_id')
        ad_name = data.get('ad_name')
        ad_message = data.get('ad_message')
        requirements = data.get('requirements')
        payroll = data.get('payroll')

        # Fetch campaign and check if it exists
        campaign = Campaign.query.filter_by(camp_id=camp_id, sponsor_id=sponsor_id).first()
        if not campaign:
            return jsonify({'status': 'error', 'message': 'Campaign not found'}), 404

        # Check if there is already an ad with the same influencer for this campaign
        # existing_ad = AdRequest.query.filter_by(camp_id=camp_id, inf_id=inf_id).first()
        # if existing_ad:
        #     return jsonify({'status': 'error', 'message': 'Ad with this influencer already exists for this campaign'}), 400

        # Fetch all ads related to this campaign and calculate total payroll
        existing_ads = AdRequest.query.filter_by(camp_id=camp_id).all()
        total_payroll = sum(ad.payroll for ad in existing_ads)

        # Calculate remaining budget
        remaining_budget = campaign.budget - total_payroll

        # Check if the payroll for the new ad exceeds the remaining budget
        if payroll > remaining_budget:
            return jsonify({'status': 'error', 'message': 'Payroll exceeds remaining budget', 'remaining_budget': remaining_budget}), 400

        # Create new AdRequest
        new_ad = AdRequest(
            ad_name=ad_name,
            camp_id=camp_id,
            inf_id=inf_id,
            messages=ad_message,
            requirements=requirements,
            payroll=payroll,
            ad_status='pending'  # Automatically set to pending
        )
        db.session.add(new_ad)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Ad created successfully'})

    # Handle preflight CORS OPTIONS request
    @cross_origin()
    def options(self):
        return '', 200

