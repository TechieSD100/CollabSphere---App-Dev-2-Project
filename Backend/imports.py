from flask import Flask, render_template, send_file, request, Response
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_cors import CORS

from datetime import datetime, timedelta

from celery_task.worker import make_celery

import os, time
from sqlalchemy import func
import requests
from celery.schedules import crontab
from jinja2 import Template


from API.Authentication.AdminAPI import *
from API.Authentication.SignupAPI import *
from API.Authentication.LoginAPI import *

from API.Admin.AdminDashboardAPI import *
from API.Admin.AdminStatsAPI import *

from API.Influencer.DashboardAPI import *
from API.Influencer.ModifyPayrollAPI import *
from API.Influencer.FindAds import *
from API.Influencer.InfluencerStats import *

from API.Sponsor.DashboardAPI import *
from API.Sponsor.CampaignsAPI import *
from API.Sponsor.AddCampaign import *
from API.Sponsor.CampaignDetails import *
from API.Sponsor.CreateAd import *
from API.Sponsor.FindInfluencer import *
from API.Sponsor.RequestForAd import *
from API.Sponsor.EditAdAPI import *
from API.Sponsor.EditCampaign import *
from API.Sponsor.SponsorStats import *

from config.security import *
from config.config import *

from models.models import *
from models.database import *


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os
import time
from httplib2 import Http
from json import dumps