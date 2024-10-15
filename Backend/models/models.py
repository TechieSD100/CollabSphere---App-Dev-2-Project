# models.py

from .database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(50), nullable=False)
    sponsor = db.relationship('Sponsor', backref='user', uselist=False)
    influencer = db.relationship('Influencer', backref='user', uselist=False)
    active = db.Column(db.Boolean, default=True)

    @property
    def id(self):
        return self.userid
    
    def __repr__(self):
        return f"User(id={self.userid}, username='{self.username}', role='{self.role}')"
    
    def get_id(self):
        return self.userid
    
    def to_dict(self):
        return {
            'userid': self.userid,
            'username': self.username,
            'role': self.role,
            'active': self.active
        }

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Role(id={self.id}, name='{self.name}', description='{self.description}')"

class Admin(User):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, db.ForeignKey('user.userid'), primary_key=True)

class Sponsor(User):
    __tablename__ = 'sponsor'
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.userid'), primary_key=True, unique=True, autoincrement=True)
    org_name = db.Column(db.String(150))
    budget = db.Column(db.Integer)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Sponsor(sponsor_id={self.sponsor_id}, org_name='{self.org_name}', budget='{self.budget}')"

class Influencer(User):
    __tablename__ = 'influencer'
    inf_id = db.Column(db.Integer, db.ForeignKey('user.userid'), primary_key=True)
    category = db.Column(db.String(150))
    niche = db.Column(db.String(150))
    reach = db.Column(db.Integer)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True, cascade='all, delete-orphan')
    flag = db.Column(db.String(150), default='unflag')

    def __repr__(self):
        return f"Influencer(inf_id={self.inf_id}, category='{self.category}', niche='{self.niche}', reach='{self.reach}')"
    

class Campaign(db.Model):
    __tablename__ = 'campaign'
    camp_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    camp_name = db.Column(db.String(150), nullable=False)
    camp_description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(150), nullable=False)
    goals = db.Column(db.String(150))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Campaign(camp_id={self.camp_id}, camp_name='{self.camp_name}', camp_description='{self.camp_description}', start_date='{self.start_date}', end_date='{self.end_date}', budget='{self.budget}', visibility='{self.visibility}', goals='{self.goals}', sponsor_id='{self.sponsor_id}')"

    

class AdRequest(db.Model):
    __tablename__ = 'adrequest'
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    ad_name = db.Column(db.String(150))
    camp_id = db.Column(db.Integer, db.ForeignKey('campaign.camp_id', ondelete='CASCADE'), nullable=False)
    inf_id = db.Column(db.Integer, db.ForeignKey('influencer.inf_id'), nullable=False)
    messages = db.Column(db.String(300))
    requirements = db.Column(db.String(150))
    payroll = db.Column(db.Integer, nullable=False)
    ad_status = db.Column(db.String(150), nullable=False)
    modified_payroll = db.Column(db.Integer)

    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', lazy=True), lazy=True)
    

    def __repr__(self):
        return f"AdRequest(ad_id='{self.ad_id}', camp_id='{self.camp_id}', inf_id='{self.inf_id}', ad_name='{self.ad_name}', payroll='{self.payroll}', modified_payroll='{self.modified_payroll}')"

