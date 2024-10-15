from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import AdRequest, Campaign, Sponsor
from flask import jsonify
from models.database import db
from io import BytesIO
import matplotlib.pyplot as plt
import base64

class MostExpensiveAdsAPI(Resource):
    @jwt_required()
    def get(self, sponsor_id):
        # Get the logged-in user's identity
        # sponsor_id = get_jwt_identity()
        
        # Query to get the most expensive ads sorted by payroll
        # ads = db.session.query(AdRequest.ad_name, AdRequest.payroll).order_by(AdRequest.payroll.desc()).limit(10).all()

        ads = db.session.query(AdRequest.ad_name, AdRequest.payroll).join(Campaign, Campaign.camp_id == AdRequest.camp_id) \
         .filter(Campaign.sponsor_id == sponsor_id) \
         .order_by(AdRequest.payroll.desc()) \
         .limit(10).all()
        
        if not ads:
            return {'status': 'error', 'message': 'No ad requests found.'}, 404
        
        ad_names = [ad.ad_name for ad in ads]
        payrolls = [ad.payroll for ad in ads]

        # Create a bar graph using matplotlib
        plt.figure(figsize=(10, 6))
        plt.barh(ad_names, payrolls, color='skyblue')
        plt.xlabel('Payroll')
        plt.title('Most Expensive Ads')
        plt.gca().invert_yaxis()  # Invert y axis to show the highest payroll at the top
        
        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        # Encode the image in base64
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        
        return {
            'status': 'success',
            'data': img_base64
        }, 200
