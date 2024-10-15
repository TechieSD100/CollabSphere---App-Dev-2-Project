# RequestForAd.py
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Influencer, User, AdRequest, Campaign
from flask import jsonify, request
from flask_cors import cross_origin
from models.database import db

class InfluencerForAdAPI(Resource):
    @jwt_required()  # Require JWT token for authentication
    @cross_origin()  # Enable cross-origin requests
    def get(self, influencer_id):
        # Fetch influencer by ID
        influencer = Influencer.query.filter_by(inf_id = influencer_id).first()
        if not influencer:
            return jsonify({'status': 'error', 'message': 'Influencer not found'}), 404
        
        # Fetch the related user information
        user = User.query.filter_by(userid = influencer_id).first()
    
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found for influencer'}), 404
    
        print(user.username)  # Logging username to Flask console

        # Prepare influencer data
        influencer_data = {
            'inf_id': influencer.inf_id,
            'username': user.username,
            'category': influencer.category,
            'niche': influencer.niche
        }
    
        return jsonify({
            'status': 'success',
            'influencer': influencer_data
        }), 200



# class FetchUnassignedAdsAPI(Resource):
#     @jwt_required()  # Require JWT token for authentication
#     @cross_origin()  # Enable cross-origin requests
#     def get(self):

#         all_ads = []
#         adreqs = AdRequest.query.filter_by(inf_id = 0)
#         if not adreqs:
#             return jsonify({'status': 'error', 'message': 'No Ads found without influencers.'}), 404

#         for ad in adreqs:
#             addetail = {
#             'ad_id': ad.ad_id,
#             'ad_name': ad.ad_name,
#             'camp_id': ad.camp_id,
#             'payroll': ad.payroll
#             }
#             all_ads.append(addetail)

#         return jsonify({
#             'status': 'success',
#             'all_ads': all_ads
#         }), 200




class FetchUnassignedAdsAPI(Resource):
    @jwt_required()  # Require JWT token for authentication
    @cross_origin()  # Enable cross-origin requests
    def get(self, sponsor_id):
        current_user_id = get_jwt_identity()  # Get the currently logged-in user's ID

        # Find the sponsor's campaigns based on the logged-in sponsor
        sponsor_campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        for c in sponsor_campaigns:
            print(c)

        if not sponsor_campaigns:
            return jsonify({'status': 'error', 'message': 'No campaigns found for this sponsor.'}), 404

        campaign_ids = [campaign.camp_id for campaign in sponsor_campaigns]

        # Fetch ad requests for the campaigns that are unassigned (inf_id=0)
        adreqs = AdRequest.query.filter(AdRequest.camp_id.in_(campaign_ids), AdRequest.inf_id == 0).all()

        if not adreqs:
            return jsonify({'status': 'error', 'message': 'No unassigned ads found for this sponsor.'}), 404

        all_ads = []
        for ad in adreqs:
            addetail = {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'payroll': ad.payroll
            }
            all_ads.append(addetail)

        return jsonify({
            'status': 'success',
            'all_ads': all_ads
        }), 200




class UpdateAdRequestAPI(Resource):
    @jwt_required()  # Require JWT token for authentication
    @cross_origin()  # Enable cross-origin requests
    def post(self):
        data = request.get_json()
        ad_id = data.get('ad_id')
        influencer_id = data.get('influencer_id')
        
        if not ad_id or not influencer_id:
            return jsonify({'status': 'error', 'message': 'ad_id or influencer_id missing'}), 400

        # Fetch the AdRequest by ad_id
        ad_request = AdRequest.query.filter_by(ad_id=ad_id).first()

        if not ad_request:
            return jsonify({'status': 'error', 'message': 'Ad Request not found'}), 404
        
        # Update the influencer ID
        ad_request.inf_id = influencer_id
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Influencer assigned successfully'}), 200
