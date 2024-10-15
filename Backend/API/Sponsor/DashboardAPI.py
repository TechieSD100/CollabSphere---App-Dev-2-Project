# SponsorDashboardAPI.py

from flask_restful import Resource
from models.models import Sponsor, Campaign, AdRequest, Influencer, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date  # Import datetime module to handle dates
from flask_cors import cross_origin
from models.database import db
from flask import request

class SponsorDetailsAPI(Resource):
    @jwt_required()  # Ensure the user is logged in
    def get(self):
        user_identity = get_jwt_identity()
        sponsor_id = user_identity['user_id']  # Extract sponsor's ID

        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()

        if sponsor:
            # Fetch all campaigns for the sponsor
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
            campaigns_data = []
            for camp in campaigns:
                # Calculate total ad payroll for the campaign
                ad_requests = AdRequest.query.filter_by(camp_id=camp.camp_id).all()
                total_payroll = sum(ad.payroll for ad in ad_requests)
                
                # Calculate percentage of budget used
                budget_used_percentage = (total_payroll / camp.budget) * 100 if camp.budget > 0 else 0

                # Calculate Day Progress Percentage
                today = date.today()
                start_date = camp.start_date
                end_date = camp.end_date

                if start_date <= today <= end_date:
                    total_days = (end_date - start_date).days
                    elapsed_days = (today - start_date).days
                    day_progress_percentage = (elapsed_days / total_days) * 100 if total_days > 0 else 0
                else:
                    day_progress_percentage = 100 if today > end_date else 0  # Campaign either hasn't started or has finished

                campaigns_data.append({
                    'camp_id': camp.camp_id,
                    'camp_name': camp.camp_name,
                    'budget': camp.budget,
                    'budget_used_percentage': round(budget_used_percentage, 2),  # Round to 2 decimal places
                    'day_progress_percentage': round(day_progress_percentage, 2),  # Day Progress Percentage
                    'status': camp.visibility  # Assuming 'visibility' field denotes status
                })
            
            return {
                'status': 'success',
                'data': {
                    'sponsor_id': sponsor.sponsor_id,
                    'org_name': sponsor.org_name,
                    'budget': sponsor.budget,
                    'campaigns': campaigns_data  # Include campaigns in response
                }
            }, 200
        else:
            return {'status': 'fail', 'message': 'Sponsor not found'}, 404
        



class ModifiedPayrollRequestAPI(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the sponsor role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        # Fetch the sponsor based on the logged-in user ID
        sponsor = Sponsor.query.filter_by(sponsor_id=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        # Fetch all ad requests for the campaigns of this sponsor where ad_status is 'modified'
        ad_requests = AdRequest.query.join(Campaign, AdRequest.camp_id == Campaign.camp_id) \
        .join(Influencer, AdRequest.inf_id == Influencer.userid) \
        .filter(Campaign.sponsor_id == sponsor.sponsor_id, AdRequest.ad_status == 'modified') \
        .all()


        # Prepare the data for the modified ad requests
        modified_ad_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name, # Campaign Name
                'username': ad.influencer.user.username,  # Influencer's Username
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
            'modified_ads': modified_ad_data
        }, 200
    




class RequestedRequestsAPI(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the sponsor role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        # Fetch the sponsor based on the logged-in user ID
        sponsor = Sponsor.query.filter_by(sponsor_id=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        # Fetch all ad requests for the campaigns of this sponsor where ad_status is 'modified'
        ad_requests = AdRequest.query.join(Campaign, AdRequest.camp_id == Campaign.camp_id) \
        .join(Influencer, AdRequest.inf_id == Influencer.userid) \
        .filter(Campaign.sponsor_id == sponsor.sponsor_id, AdRequest.ad_status == 'requested') \
        .all()


        # Prepare the data for the modified ad requests
        requested_ad_data = [
            {
                'ad_id': ad.ad_id,
                'ad_name': ad.ad_name,
                'camp_id': ad.camp_id,
                'camp_name': ad.campaign.camp_name, # Campaign Name
                'username': ad.influencer.user.username,  # Influencer's Username
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
            'requested_ads': requested_ad_data
        }, 200
    



class UpdateAdStatusAPI(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        """
        Update the status of an AdRequest based on sponsor's action.

        Expected JSON Payload:
        {
            "ad_id": <int>,
            "action": "accept" or "reject"
        }
        """
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the sponsor role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        # Fetch the sponsor based on the logged-in user ID
        sponsor = Sponsor.query.filter_by(sponsor_id=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        data = request.get_json()

        ad_id = data.get('ad_id')
        action = data.get('action')

        if not ad_id or not action:
            return {'status': 'fail', 'message': 'ad_id and action are required.'}, 400

        # Fetch the AdRequest
        ad_request = AdRequest.query.join(Campaign).filter(
            AdRequest.ad_id == ad_id,
            Campaign.sponsor_id == sponsor.sponsor_id
        ).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'AdRequest not found or unauthorized.'}, 404

        if action == 'accept':
            if ad_request.modified_payroll is None:
                return {'status': 'fail', 'message': 'No modified payroll to accept.'}, 400
            ad_request.payroll = ad_request.modified_payroll
            ad_request.modified_payroll = None
            ad_request.ad_status = 'accepted'
        elif action == 'reject':
            ad_request.modified_payroll = -1
            ad_request.ad_status = 'pending'
        else:
            return {'status': 'fail', 'message': 'Invalid action. Use "accept" or "reject".'}, 400

        try:
            db.session.commit()
            return {'status': 'success', 'message': f'AdRequest {action}ed successfully.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'message': 'An error occurred while updating the AdRequest.'}, 500





class UpdateRequestedAdStatusAPI(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        """
        Update the status of an AdRequest based on sponsor's action.

        Expected JSON Payload:
        {
            "ad_id": <int>,
            "action": "accept" or "reject"
        }
        """
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure that the user has the sponsor role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        # Fetch the sponsor based on the logged-in user ID
        sponsor = Sponsor.query.filter_by(sponsor_id=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        data = request.get_json()

        ad_id = data.get('ad_id')
        action = data.get('action')

        if not ad_id or not action:
            return {'status': 'fail', 'message': 'ad_id and action are required.'}, 400

        # Fetch the AdRequest
        ad_request = AdRequest.query.join(Campaign).filter(
            AdRequest.ad_id == ad_id,
            Campaign.sponsor_id == sponsor.sponsor_id
        ).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'AdRequest not found or unauthorized.'}, 404

        if action == 'accept':
            ad_request.modified_payroll = None
            ad_request.ad_status = 'accepted'
        elif action == 'reject':
            ad_request.modified_payroll = -1
            ad_request.ad_status = 'rejected'
        else:
            return {'status': 'fail', 'message': 'Invalid action. Use "accept" or "reject".'}, 400

        try:
            db.session.commit()
            return {'status': 'success', 'message': f'Ad Collaboration Request {action}ed successfully.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'message': 'An error occurred while updating the AdRequest.'}, 500
