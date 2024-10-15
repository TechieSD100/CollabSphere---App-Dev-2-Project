# AdminStatsAPI.py 

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import AdRequest, Admin
from flask import jsonify
from models.database import db
from io import BytesIO
import matplotlib.pyplot as plt
import base64

class AdStatusPieChartAPI(Resource):
    @jwt_required()
    def get(self):
        # Get the logged-in user's identity
        user_identity = get_jwt_identity()
        
        # Define the possible statuses
        statuses = ['modified', 'pending', 'accepted', 'rejected', 'requested']
        
        # Initialize counts
        status_counts = {status: 0 for status in statuses}
        
        # Query counts
        counts = db.session.query(AdRequest.ad_status, db.func.count(AdRequest.ad_id)).group_by(AdRequest.ad_status).all()
        
        for status, count in counts:
            if status in status_counts:
                status_counts[status] = count
        
        # Create the pie chart using matplotlib
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        
        # Only include statuses with count > 0
        labels = [label for label, size in zip(labels, sizes) if size > 0]
        sizes = [size for size in sizes if size > 0]
        
        # Define colors
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        
        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors[:len(labels)])
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Ad Status Distribution')
        
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