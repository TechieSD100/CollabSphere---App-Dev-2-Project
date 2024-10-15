# api/EditAdAPI.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Sponsor, Campaign, AdRequest, Influencer
from flask import jsonify
from models.database import db

class AdRequestDetailsAPI(Resource):
    @jwt_required()
    def get(self, ad_id):
        """
        Get details of a specific AdRequest for editing.
        Only the sponsor who owns the campaign can access.
        """
        user_identity = get_jwt_identity()
        user_id = user_identity.get('user_id')
        user_role = user_identity.get('role')

        # Ensure the user has the 'sponsor' role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        sponsor = Sponsor.query.filter_by(userid=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        # Fetch the AdRequest
        ad_request = AdRequest.query.filter_by(ad_id=ad_id).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'Ad request not found.'}, 404

        # Fetch the campaign associated with this AdRequest
        campaign = Campaign.query.filter_by(camp_id=ad_request.camp_id).first()

        if not campaign or campaign.sponsor_id != sponsor.sponsor_id:
            return {'status': 'fail', 'message': 'You do not have permission to access this Ad Request.'}, 403

        # Fetch all influencers for the dropdown
        influencers = Influencer.query.all()
        influencers_data = [
            {
                'inf_id': inf.inf_id,
                'username': inf.user.username,
                'category': inf.category,
                'niche': inf.niche,
                'reach': inf.reach
            }
            for inf in influencers
        ]

        ad_request_data = {
            'ad_id': ad_request.ad_id,
            'ad_name': ad_request.ad_name,
            'camp_id': ad_request.camp_id,
            'ad_message': ad_request.messages,
            'requirements': ad_request.requirements,
            'payroll': ad_request.payroll,
            'ad_status': ad_request.ad_status,
            'modified_payroll': ad_request.modified_payroll,
            'inf_id': ad_request.inf_id if ad_request.inf_id else 0,  # 0 for "Yet to be decided"
            'influencers': influencers_data
        }

        return {
            'status': 'success',
            'data': ad_request_data
        }, 200

    @jwt_required()
    def put(self, ad_id):
        """
        Update an existing AdRequest.
        Only the sponsor who owns the campaign can update.
        """
        user_identity = get_jwt_identity()
        user_id = user_identity.get('user_id')
        user_role = user_identity.get('role')

        # Ensure the user has the 'sponsor' role
        if user_role != 'sponsor':
            return {'status': 'fail', 'message': 'Access restricted to sponsors only.'}, 403

        sponsor = Sponsor.query.filter_by(userid=user_id).first()

        if not sponsor:
            return {'status': 'fail', 'message': 'Sponsor not found.'}, 404

        # Fetch the AdRequest
        ad_request = AdRequest.query.filter_by(ad_id=ad_id).first()

        if not ad_request:
            return {'status': 'fail', 'message': 'Ad request not found.'}, 404

        # Fetch the campaign associated with this AdRequest
        campaign = Campaign.query.filter_by(camp_id=ad_request.camp_id).first()

        if not campaign or campaign.sponsor_id != sponsor.sponsor_id:
            return {'status': 'fail', 'message': 'You do not have permission to update this Ad Request.'}, 403

        # Parse the incoming JSON data
        parser = reqparse.RequestParser()
        parser.add_argument('ad_name', type=str, required=True, help='Ad Name is required.')
        parser.add_argument('ad_message', type=str, required=False)
        parser.add_argument('requirements', type=str, required=False)
        parser.add_argument('payroll', type=int, required=True, help='Payroll is required.')
        parser.add_argument('inf_id', type=int, required=True, help='Influencer ID is required.')
        args = parser.parse_args()

        # Validate the influencer ID
        inf_id = args.get('inf_id')
        if inf_id != 0:
            influencer = Influencer.query.filter_by(inf_id=inf_id).first()
            if not influencer:
                return {'status': 'fail', 'message': 'Influencer not found.'}, 404
        else:
            influencer = None

        # Update the AdRequest fields
        ad_request.ad_name = args.get('ad_name')
        ad_request.messages = args.get('ad_message', '')
        ad_request.requirements = args.get('requirements', '')
        ad_request.payroll = args.get('payroll')
        ad_request.inf_id = inf_id if inf_id != 0 else 0
        ad_request.ad_status = 'requested' if inf_id != 0 else 'pending'  # Set status based on assignment

        try:
            db.session.commit()
            return {'status': 'success', 'message': 'Ad request updated successfully.'}, 200
        except Exception as e:
            db.session.rollback()
            # Log the exception if necessary
            return {'status': 'fail', 'message': 'An error occurred while updating the ad request.'}, 500
