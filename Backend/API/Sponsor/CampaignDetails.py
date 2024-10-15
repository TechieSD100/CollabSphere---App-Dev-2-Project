# CampaignDetails.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Sponsor, Campaign, AdRequest
from flask import jsonify, request
from models.database import db

class CampaignDetailsAPI(Resource):
    @jwt_required()  # Ensure the sponsor is logged in
    def get(self, campaign_id):
        user_identity = get_jwt_identity()

        sponsor = Sponsor.query.filter_by(userid=user_identity['user_id']).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404

        campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id=sponsor.sponsor_id).first()

        if not campaign:
            return {'status': 'fail', 'message': 'Campaign not found'}, 404

        ad_requests = AdRequest.query.filter_by(camp_id=campaign_id).all()

        ad_requests1 = AdRequest.query.filter(AdRequest.camp_id == campaign_id, AdRequest.ad_status != 'rejected').all()
        #excludes the ads that got rejected in calculation of remaining

        total_payroll = sum(ad.payroll for ad in ad_requests1)

        ad_requests_data = []
        for ad in ad_requests:
            username = ad.influencer.user.username if ad.inf_id else "Yet to be decided"
            ad_requests_data.append({
                'ad_id': ad.ad_id,
                'ad_title': ad.ad_name,
                'status': ad.ad_status,
                'payroll': ad.payroll,
                'inf_name': username,
                'ad_message': ad.messages,
                'requirements': ad.requirements
            })

        campaign_data = {
            'camp_id': campaign.camp_id,
            'camp_name': campaign.camp_name,
            'camp_description': campaign.camp_description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'total_payroll': total_payroll,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'ad_requests': ad_requests_data
        }

        return jsonify({
            'status': 'success',
            'data': campaign_data
        })



class DeleteAdRequestAPI(Resource):
    @jwt_required()
    def delete(self, ad_id):
        # Fetch the ad request to delete
        ad_request = AdRequest.query.filter_by(ad_id=ad_id).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'Ad request not found'}, 404

        # Delete the ad request
        db.session.delete(ad_request)
        db.session.commit()

        return {'status': 'success', 'message': 'Ad request deleted successfully'}