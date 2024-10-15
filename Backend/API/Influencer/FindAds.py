# FindAds.py


from flask_restful import Resource
from models.database import db
from models.models import AdRequest, Campaign, Influencer
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from flask import jsonify, request

class AdSearchAPI(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        user_identity = get_jwt_identity()

        search_query = request.args.get('query', '').lower()

        ads_all = []
        ads_name = []
        ads_campaign = []
        ads_requirements = []

        ads0 = AdRequest.query.all()
        ads1 = AdRequest.query.filter(AdRequest.ad_name.ilike(f"%{search_query}%")).all()
        ads2 = AdRequest.query.filter(Campaign.camp_name.ilike(f"%{search_query}%")).all()
        ads3 = AdRequest.query.filter(AdRequest.requirements.ilike(f"%{search_query}%")).all()

        if search_query == "":
            ads1 = []
            ads2 = []
            ads3 = []

        # Takes all ads
        for ad in ads0:
            campaign = Campaign.query.filter_by(camp_id = ad.camp_id).first()
            
            if campaign.visibility != 'private' and ad.inf_id == 0:
                addetails = {
                    'ad_id': ad.ad_id,
                    'ad_name': ad.ad_name,
                    'camp_id': ad.camp_id,
                    'camp_name': campaign.camp_name,
                    'message': ad.messages,
                    'requirements': ad.requirements,
                    'payroll': ad.payroll
                }
                ads_all.append(addetails)


        # Takes ads by ad name search
        for ad in ads1:
            campaign = Campaign.query.filter_by(camp_id = ad.camp_id).first()
            
            if campaign.visibility != 'private' and ad.inf_id == 0:
                addetails = {
                    'ad_id': ad.ad_id,
                    'ad_name': ad.ad_name,
                    'camp_id': ad.camp_id,
                    'camp_name': campaign.camp_name,
                    'message': ad.messages,
                    'requirements': ad.requirements,
                    'payroll': ad.payroll
                }
                ads_name.append(addetails)



        # Takes ads by campaign name search
        for ad in ads2:
            campaign = Campaign.query.filter_by(camp_id = ad.camp_id).first()
            
            if campaign.visibility != 'private' and ad.inf_id == 0:
                addetails = {
                    'ad_id': ad.ad_id,
                    'ad_name': ad.ad_name,
                    'camp_id': ad.camp_id,
                    'camp_name': campaign.camp_name,
                    'message': ad.messages,
                    'requirements': ad.requirements,
                    'payroll': ad.payroll
                }
                ads_campaign.append(addetails)



        # Takes ads by requirements search
        for ad in ads3:
            campaign = Campaign.query.filter_by(camp_id = ad.camp_id).first()
            
            if campaign.visibility != 'private' and ad.inf_id == 0:
                addetails = {
                    'ad_id': ad.ad_id,
                    'ad_name': ad.ad_name,
                    'camp_id': ad.camp_id,
                    'camp_name': campaign.camp_name,
                    'message': ad.messages,
                    'requirements': ad.requirements,
                    'payroll': ad.payroll
                }
                ads_requirements.append(addetails)


        return jsonify({
            'status': 'success',
            'ads_all': ads_all,
            'ads_name': ads_name,
            'ads_campaign': ads_campaign,
            'ads_requirements': ads_requirements
        })
    




class JoinAdAPI(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, ad_id):
        """
        Handle the "Request to Join" action.
        """
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        # Ensure the user has the 'influencer' role
        if user_role != 'influencer':
            return jsonify({'status': 'fail', 'message': 'Access restricted to influencers only.'}), 403

        # Fetch the influencer record
        influencer = Influencer.query.filter_by(inf_id=user_id).first()

        if not influencer:
            return jsonify({'status': 'fail', 'message': 'Influencer not found.'}), 404

        # Fetch the specific ad request
        ad_request = AdRequest.query.filter_by(ad_id=ad_id).first()

        if not ad_request:
            return jsonify({'status': 'fail', 'message': 'Ad request not found.'}), 404

        # Check if the ad is already assigned to an influencer
        if ad_request.inf_id is not None and ad_request.inf_id != 0:
            return jsonify({'status': 'fail', 'message': 'This ad is already assigned to an influencer.'}), 400

        # Optionally, you might want to check if the current user has already requested this ad
        # This depends on your application's logic

        # Update the ad_request with the current influencer's ID and set status to 'requested'
        ad_request.inf_id = influencer.inf_id
        ad_request.ad_status = 'requested'

        try:
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Ad request submitted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'fail', 'message': 'An error occurred while submitting the ad request.'}), 500