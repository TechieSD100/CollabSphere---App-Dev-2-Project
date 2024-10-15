from models.models import Campaign , Influencer
from Cache.cache import cache
from flask_jwt_extended import jwt_required




@jwt_required()
@cache.cached(timeout=10)
def get_all_campaigns(sponsor_id):
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
    return campaigns



@jwt_required()
@cache.memoize(10)
def get_all_influencers():
    influencers = Influencer.query.all()
    return influencers