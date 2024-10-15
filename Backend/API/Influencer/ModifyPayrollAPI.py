from flask_restful import Resource, reqparse
from models.models import User, Influencer, AdRequest, Campaign, Sponsor
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db

class ModifyPayrollAPI(Resource):
    @jwt_required()
    def post(self, ad_id):
        """
        Modify the payroll for a specific ad request.
        Expected JSON payload:
        {
            "modified_payroll": <integer>
        }
        """
        parser = reqparse.RequestParser()
        parser.add_argument('modified_payroll', type=int, required=True, help="Modified payroll is required and should be an integer.")
        args = parser.parse_args()

        modified_payroll = args.get('modified_payroll')

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
            return {'status': 'fail', 'message': f"Cannot modify payroll. Current status is '{ad_request.ad_status}'."}, 400

        # Update the modified_payroll and ad_status
        ad_request.modified_payroll = modified_payroll
        ad_request.ad_status = 'modified'

        try:
            db.session.commit()
            return {'status': 'success', 'message': "Payroll modified successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'message': 'An error occurred while modifying the payroll.'}, 500

    @jwt_required()
    def get(self, ad_id):
        """
        (Optional) Fetch details of a specific ad request.
        """
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

        # Fetch related campaign and sponsor details
        campaign = Campaign.query.filter_by(camp_id=ad_request.camp_id).first()
        sponsor = Sponsor.query.filter_by(sponsor_id=campaign.sponsor_id).first()

        ad_request_data = {
            'ad_id': ad_request.ad_id,
            'ad_name': ad_request.ad_name,
            'camp_id': ad_request.camp_id,
            'camp_name': campaign.camp_name if campaign else '',
            'sponsor_name': sponsor.org_name if sponsor else '',
            'messages': ad_request.messages,
            'requirements': ad_request.requirements,
            'payroll': ad_request.payroll,
            'modified_payroll': ad_request.modified_payroll,
            'ad_status': ad_request.ad_status
        }

        return {
            'status': 'success',
            'ad_request': ad_request_data
        }, 200
