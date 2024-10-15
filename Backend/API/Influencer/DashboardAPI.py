# InfluencerAPI.py

from flask_restful import Resource, reqparse
from models.models import User, Influencer, AdRequest, Campaign, Sponsor
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db

class InfluencerDetailsAPI(Resource):
    @jwt_required()  # Ensure the user is logged in
    def get(self):
        user_identity = get_jwt_identity()
        inf_id = user_identity['user_id']  # Extract influencer's ID

        influencer = Influencer.query.filter_by(inf_id=inf_id).first()

        if influencer:
            user = User.query.filter_by(userid=inf_id).first()
            return {
                'status': 'success',
                'data': {
                    'inf_id': influencer.inf_id,
                    'username': user.username,
                    'category': influencer.category,
                    'niche': influencer.niche,
                    'reach': influencer.reach,
                    'flag': influencer.flag
                }
            }, 200
        else:
            return {'status': 'fail', 'message': 'Influencer not found'}, 404



class PendingAdRequestsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch all pending ad requests for this influencer, including campaign and sponsor details
        ad_requests = AdRequest.query.filter_by(inf_id=user_id, ad_status='pending') \
            .join(Campaign) \
            .join(Sponsor) \
            .all()

        ad_requests_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name,          # Campaign Name
                'sponsor_name': ad.campaign.sponsor.org_name,  # Sponsor Name
                'messages': ad.messages,
                'requirements': ad.requirements,
                'payroll': ad.payroll,
                'ad_status': ad.ad_status,
                'modified_payroll': ad.modified_payroll
            }
            for ad in ad_requests
        ]

        return {
            'status': 'success',
            'ad_requests': ad_requests_data
        }, 200
    



class ModifiedRequestsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch all pending ad requests for this influencer, including campaign and sponsor details
        ad_requests = AdRequest.query.filter_by(inf_id=user_id, ad_status='modified') \
            .join(Campaign) \
            .join(Sponsor) \
            .all()

        modified_ad_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name,          # Campaign Name
                'sponsor_name': ad.campaign.sponsor.org_name,  # Sponsor Name
                # 'messages': ad.messages,
                # 'requirements': ad.requirements,
                'payroll': ad.payroll,
                # 'ad_status': ad.ad_status,
                'modified_payroll': ad.modified_payroll
            }
            for ad in ad_requests
        ]

        return {
            'status': 'success',
            'modified_ads': modified_ad_data
        }, 200
    



class RequestedAdRequestsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch all pending ad requests for this influencer, including campaign and sponsor details
        ad_requests = AdRequest.query.filter_by(inf_id=user_id, ad_status='requested') \
            .join(Campaign) \
            .join(Sponsor) \
            .all()

        ad_requests_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name,          # Campaign Name
                'sponsor_name': ad.campaign.sponsor.org_name,  # Sponsor Name
                'messages': ad.messages,
                'requirements': ad.requirements,
                'payroll': ad.payroll,
                'ad_status': ad.ad_status,
                # 'modified_payroll': ad.modified_payroll
            }
            for ad in ad_requests
        ]

        return {
            'status': 'success',
            'requested_requests': ad_requests_data
        }, 200




class RejectedRequestsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch all pending ad requests for this influencer, including campaign and sponsor details
        ad_requests = AdRequest.query.filter_by(inf_id=user_id, ad_status='rejected') \
            .join(Campaign) \
            .join(Sponsor) \
            .all()

        rejected_ad_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name,          # Campaign Name
                'sponsor_name': ad.campaign.sponsor.org_name,  # Sponsor Name
                'messages': ad.messages,
                'requirements': ad.requirements,
                'payroll': ad.payroll,
                'ad_status': ad.ad_status,
                'modified_payroll': ad.modified_payroll
            }
            for ad in ad_requests
        ]

        return {
            'status': 'success',
            'rejected_ads': rejected_ad_data
        }, 200




class ActiveAdsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch all pending ad requests for this influencer, including campaign and sponsor details
        ad_requests = AdRequest.query.filter_by(inf_id=user_id, ad_status='accepted') \
            .join(Campaign) \
            .join(Sponsor) \
            .all()

        active_ads = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name,          # Campaign Name
                'sponsor_name': ad.campaign.sponsor.org_name,  # Sponsor Name
                'messages': ad.messages,
                'requirements': ad.requirements,
                'payroll': ad.payroll,
                'ad_status': ad.ad_status,
                'modified_payroll': ad.modified_payroll
            }
            for ad in ad_requests
        ]

        return {
            'status': 'success',
            'active_ads': active_ads
        }, 200




class UpdateAdRequestStatusAPI(Resource):
    @jwt_required()
    def post(self, ad_id):
        """
        Update the status of an ad request.
        Expected JSON payload:
        {
            "action": "accept" | "reject"
        }
        """
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, help="Action ('accept' or 'reject') is required.")
        args = parser.parse_args()

        action = args.get('action').lower()

        if action not in ['accept', 'reject']:
            return {'status': 'fail', 'message': "Invalid action. Must be 'accept' or 'reject'."}, 400

        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the influencer role
        if user_role != 'influencer':
            return {'status': 'fail', 'message': 'Access restricted to influencers only.'}, 403

        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return {'status': 'fail', 'message': 'Influencer not found.'}, 404

        # Fetch the specific ad request
        ad_request = AdRequest.query.filter_by(ad_id=ad_id, inf_id=user_id).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'Ad request not found.'}, 404

        if ad_request.ad_status != 'pending':
            return {'status': 'fail', 'message': f"Cannot perform action. Current status is '{ad_request.ad_status}'."}, 400

        # Update the ad_status based on the action
        if action == 'accept':
            ad_request.ad_status = 'accepted'
            ad_request.modified_payroll = None
        elif action == 'reject':
            ad_request.ad_status = 'rejected'
            ad_request.modified_payroll = None

        try:
            db.session.commit()
            return {'status': 'success', 'message': f"Ad request {action}ed successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'message': 'An error occurred while updating the ad request.'}, 500