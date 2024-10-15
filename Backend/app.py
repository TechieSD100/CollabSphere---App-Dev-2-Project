# app.py

from imports import *

def create_app():
    app_create = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app_create.config.update(
            CELERY_BROKER_URL='redis://localhost:6379',
            CELERY_RESULT_BACKEND='redis://localhost:6379'
        )
        celery_app = make_celery(app_create)
        app_create.config.from_object(LocalDevelopmentConfig)

    # Adjust CORS to allow all methods from any origin for now
    CORS(app_create, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app_create)
    api_create = Api(app_create)
    JWTManager(app_create)
    security.init_app(app_create, user_datastore)
    cache.init_app(app_create)
    app_create.app_context().push()
    
    return app_create, api_create , celery_app

app, api , celery  = create_app()





##______________________________________CELERY TASKS----ALL TASKS OF CELERY____________________________________________##

           ######_______________________EXPORT CSV TASK - USER TRIGGERED_______________________######
@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b

@celery.task
def generate_csv_file(camp_id):
    import csv

    #time.sleep(6)
    ad_requests = AdRequest.query.filter_by(camp_id = camp_id).all()

    ad_requests1 = []

    for ad in ad_requests:
        ad_id = ad.ad_id
        ad_name = ad.ad_name
        status = ad.ad_status
        payroll = ad.payroll

        ad_info = {ad_id,ad_name,status,payroll}
        ad_requests1.append(ad_info)

    with open("static/details.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ad ID', 'Ad Name', 'Ad Status', 'Payroll'])
        for c_data in ad_requests1:
            writer.writerow(c_data)

    return "Export Job Started.."



class Trigger(Resource):
    def get(self, campaign_id):
        a=generate_csv_file.delay(campaign_id)
        return {
            "Task_ID": a.id,
            "Task_State": a.state,
            "Task_Result": a.result  
        }
        
class Download(Resource):
    def get(self):
        return send_file('static/details.csv', as_attachment=True)
               




@celery.on_after_finalize.connect
def daily_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(45, send_Daily_mail.s(), name = "Daily Evening")
    #sender.add_periodic_task(crontab(hour=3, minute=38), send_Daily_mail.s(), name = "Daily Evening")
    sender.add_periodic_task(crontab(hour=16, minute=39, day_of_month=2), SendMonthlyReport.s(), name = "2nd of every month")
    sender.add_periodic_task(30 , add_together.s(1,2), name = "Add Together")



@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b


@celery.task
def send_Daily_mail():
    # Fetch influencers with pending ad requests
    pending_ad_requests = AdRequest.query.filter_by(ad_status='pending').all()
    
    # Collect influencer emails
    influencer_emails = set()  # Use a set to avoid duplicates

    for ad_request in pending_ad_requests:
        influencer = Influencer.query.filter_by(inf_id=ad_request.inf_id).first()
        user = User.query.filter_by(userid=influencer.inf_id).first()  # Fetch user to get email
        if user:
            influencer_emails.add(user.username)

    # for email in influencer_emails:
    send_email(
        to_address="dummy@gmail.com",
        subject="Test Email",
        message="This is a test email from MailHog."
    )




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@infcamp.com"
SENDER_PASSWORD = ""  # Usually not needed for MailHog

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    with smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT) as s:
        # s.login(SENDER_ADDRESS, SENDER_PASSWORD)  # Comment out if MailHog does not require login
        s.send_message(msg)


def format_message(template_file, data={}, bookings=[]):

    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1]+ "-" + str(currentYear)

    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, bookings=bookings)

#-------------------------------------------------------------------------------------------------------------------------
     ###_______________________CELERY TASK SCHEDULAR - MONTHLY Buy REPORT______________________###



def format_message(template_file, data={}, bookings=[]):

    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1]+ "-" + str(currentYear)

    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, bookings=bookings)

def get_user_bookings(sponsor_id):
    today = datetime.utcnow()
    currentmonth= today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor_id).all()

    ad_requests = []
    for ad_request in ad_requests:
        campaign_name = ad_request.campaign.camp_name
        ad_name = ad_request.ad_name 
        camp_status = ad_request.camp_status

        ad_info = {
            'campaign_name': campaign_name,
            'ad_name': ad_name,
            'camp Status': camp_status,
        }
        ad_requests.append(ad_info)

    return ad_requests

def send_monthly_report_email(data, lastmonth):
    sponsor_id = data.id  
    bookings = get_user_bookings(sponsor_id, lastmonth)


    message = format_message("monthly_report.html", lastmonth=lastmonth, data=data, bookings=bookings)
    send_email(data.email, subject="Monthly Report", message=message)


@celery.task()
def SendMonthlyReport():
    print("Starting SendMonthlyReport Task")

    users = Sponsor.query.all()
    

    today = datetime.utcnow()
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    last_month = first_day_of_previous_month

    for user in users:
        send_monthly_report_email(data=user, lastmonth=last_month)






# Add the routes here
api.add_resource(AdminLoginAPI, '/api/admin-login')
api.add_resource(SignupAdminAPI, '/api/admin-signup')
api.add_resource(SignupInfluencerAPI, '/api/influencer-signup')
api.add_resource(SignupSponsorAPI, '/api/sponsor-signup')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(InfluencerDetailsAPI, '/api/influencer-details')
api.add_resource(PendingAdRequestsAPI, '/api/influencer/pending-ad-requests')
api.add_resource(UpdateAdRequestStatusAPI, '/api/influencer/ad-request/<int:ad_id>/update')
api.add_resource(ModifyPayrollAPI, '/api/adrequest/<int:ad_id>/modify-payroll')
api.add_resource(SponsorDetailsAPI, '/api/sponsor-details')
api.add_resource(CampaignsAPI, '/api/sponsor-campaigns')
api.add_resource(AddCampaignAPI, '/api/add-campaign')
api.add_resource(FetchInfluencerAPI, '/api/fetch-influencers')
api.add_resource(CreateAdAPI, '/api/create-ad')
api.add_resource(InfluencerSearchAPI, '/api/influencer-search')
api.add_resource(InfluencerForAdAPI, '/api/influencer/<int:influencer_id>')
api.add_resource(FetchUnassignedAdsAPI, '/api/ads/unassigned/<int:sponsor_id>')
api.add_resource(UpdateAdRequestAPI, '/api/adrequest/update')
api.add_resource(CampaignDetailsAPI, '/api/campaign-details/<int:campaign_id>', '/api/campaign-details/<int:campaign_id>/ad/<int:ad_id>')
api.add_resource(DeleteAdRequestAPI, '/api/delete-ad/<int:ad_id>')
api.add_resource(PendingSponsorAPI, '/api/pending-sponsor-signup')
api.add_resource(ApproveSponsorAPI, '/api/approve-sponsor/<int:sponsor_id>')
api.add_resource(DeclineSponsorAPI, '/api/decline-sponsor/<int:sponsor_id>')
api.add_resource(DeclinedSponsorsListAPI, '/api/declined-sponsors-list')
api.add_resource(ValidateSponsorAPI, '/api/validate-sponsor/<int:sponsor_id>')
api.add_resource(ModifiedRequestsAPI, '/api/influencer/modified-ad-requests')
api.add_resource(RejectedRequestsAPI, '/api/influencer/rejected-ad-requests')
api.add_resource(ActiveAdsAPI, '/api/influencer/active-ads')
api.add_resource(RequestedAdRequestsAPI, '/api/influencer/requested-ads')
api.add_resource(ModifiedPayrollRequestAPI, '/api/sponsor/modified-payroll-requests')
api.add_resource(RequestedRequestsAPI, '/api/sponsor/influencer-requested-requests')
api.add_resource(UpdateAdStatusAPI, '/api/sponsor/update-ad-status')
api.add_resource(UpdateRequestedAdStatusAPI, '/api/sponsor/update-requested-ad-status')
api.add_resource(AdSearchAPI, '/api/ads-search')
api.add_resource(JoinAdAPI, '/api/ads/<int:ad_id>/join')
api.add_resource(AdRequestDetailsAPI, '/api/ad-request/<int:ad_id>')
api.add_resource(CampaignDetailAPI, '/api/sponsor-campaigns/<int:camp_id>') #deletion of campaign API
api.add_resource(EditCampaignsAPI, '/api/edit-campaign/<int:camp_id>')
api.add_resource(AdStatusPieChartAPI, '/api/ad-status-piechart') 
api.add_resource(Trigger, '/api/trigger/<int:campaign_id>')
api.add_resource(Download, '/api/download')
api.add_resource(MostExpensiveAdsAPI, '/api/most-expensive-ads/<int:sponsor_id>')
api.add_resource(AllInfluencersAPI, '/api/all-influencers')
api.add_resource(FlagInfluencerAPI, '/api/flag-influencer/<int:inf_id>')
api.add_resource(UnflagInfluencerAPI, '/api/unflag-influencer/<int:inf_id>')
api.add_resource(PopularCampaignsAPI, '/api/popular-campaigns')




if __name__ == "__main__":
    app.run(debug=True)
