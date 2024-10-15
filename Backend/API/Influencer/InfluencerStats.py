from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.models import AdRequest, Campaign
from flask import jsonify
from models.database import db
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from collections import Counter

class PopularCampaignsAPI(Resource):
    @jwt_required()
    def get(self):
        # Query all AdRequests
        ad_requests = AdRequest.query.all()

        # Count frequency of each camp_id
        camp_id_counts = Counter([ad_request.camp_id for ad_request in ad_requests])

        if not camp_id_counts:
            return {
                'status': 'fail',
                'message': 'No Ad Requests found.'
            }, 404

        # Fetch campaign names
        campaigns = Campaign.query.filter(Campaign.camp_id.in_(camp_id_counts.keys())).all()
        camp_id_to_name = {campaign.camp_id: campaign.camp_name for campaign in campaigns}

        # Prepare data for the pie chart
        labels = []
        sizes = []
        for camp_id, count in camp_id_counts.items():
            camp_name = camp_id_to_name.get(camp_id, f'Campaign {camp_id}')
            labels.append(camp_name)
            sizes.append(count)

        # Generate pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Most Common Campaigns Based on Ad Requests')

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        # Encode the image in base64
        plot_url = base64.b64encode(img.getvalue()).decode()

        return {
            'status': 'success',
            'image': plot_url
        }, 200
