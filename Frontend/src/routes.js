// routes.js

import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from './components/UserLogin.vue'
import AdminLogin from './components/AdminLogin.vue'
import SponsorSignUp from './components/SponsorSignUp.vue'
import InfluencerSignUp from './components/InfluencerSignUp.vue'
import AdminDashboard from './components/Admin/AdminDashboard.vue'
import SponsorDashboard from './components/Sponsor/SponsorDashboard.vue'
import InfluencerDashboard from './components/Influencer/InfluencerDashboard.vue'
import AddCampaign from './components/Sponsor/AddCampaign.vue';
import SponsorCampaigns from './components/Sponsor/SponsorCampaigns.vue'
import CampaignDetails from './components/Sponsor/CampaignDetails.vue'
import CreateAd from './components/Sponsor/CreateAd.vue'
import FindInfluencer from './components/Sponsor/FindInfluencer.vue'
import RequestForAd from './components/Sponsor/RequestForAd.vue'
import ModifyPayroll from './components/Influencer/ModifyPayroll.vue'
import FindAds from './components/Influencer/FindAds.vue'
import EditAd from './components/Sponsor/EditAd.vue'
import EditCampaign from './components/Sponsor/EditCampaign.vue'
import AdminStats from './components/Admin/AdminStats.vue'
import SponsorStats from './components/Sponsor/SponsorStats.vue'
import InfluencerStats from './components/Influencer/InfluencerStats.vue'

// Define the routes
const routes = [
    { path: '/', redirect: '/user-login' },
    { name: 'UserLogin', component: UserLogin, path: '/user-login' },
    { name: 'AdminLogin', component: AdminLogin, path: '/admin-login' },
    { name: 'SponsorSignUp', component: SponsorSignUp, path: '/sponsor-signup' },
    { name: 'InfluencerSignUp', component: InfluencerSignUp, path: '/influencer-signup' },
    { name: 'AdminDashboard', component: AdminDashboard, path: '/admin-dashboard' },
    { name: 'SponsorDashboard', component: SponsorDashboard, path: '/sponsor-dashboard/:sponsor_id' },
    { name: 'InfluencerDashboard', component: InfluencerDashboard, path: '/influencer-dashboard/:inf_id' },
    { name: 'SponsorCampaigns', component: SponsorCampaigns, path: '/sponsor-campaigns/:sponsor_id'},
    { name: 'AddCampaign', component: AddCampaign, path: '/sponsor-campaigns/:sponsor_id/add-campaign' },
    { name: 'CampaignDetails', component: CampaignDetails, path: '/sponsor-campaigns/:sponsor_id/campaign-details/:campaign_id' },
    { name: 'CreateAd', component: CreateAd, path: '/sponsor-campaigns/:sponsor_id/campaign-details/:campaign_id/create-ad'},
    { name: 'FindInfluencer', component: FindInfluencer, path: '/find-influencer/:sponsor_id'},
    { name: 'RequestForAd', component: RequestForAd, path: '/find-influencer/:sponsor_id/ad-request/:influencer_id' },
    { name: 'ModifyPayroll', component: ModifyPayroll, path: '/modify-payroll/:ad_id' },
    { name: 'FindAds', component: FindAds, path: '/find-ads/:inf_id' },
    { name: 'EditAd', component: EditAd, path: '/sponsor-campaigns/:sponsor_id/campaign-details/:campaign_id/edit-ad/:ad_id' },
    { name: 'EditCampaign', component: EditCampaign, path: '/sponsor-campaigns/:sponsor_id/edit-campaign/:campaign_id' },
    { name: 'AdminStats', component: AdminStats, path: '/admin-stats' },
    { name: 'SponsorStats', component: SponsorStats, path: '/sponsor-stats/:sponsor_id' },
    { name: 'InfluencerStats', component: InfluencerStats, path: '/influencer-stats/:inf_id'}
];

// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes
});

// Navigation guard
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');

    if (to.name === 'AdminDashboard' && (!token || userRole !== 'admin')) {
        // Redirect to login if not admin
        next('/admin-login');
    } else if (to.name === 'SponsorDashboard' && (!token || userRole !== 'sponsor')) {
        // Redirect to login if not sponsor
        next('/user-login');
    } else if (to.name === 'InfluencerDashboard' && (!token || userRole !== 'influencer')) {
        // Redirect to login if not influencer
        next('/user-login');
    } else {
        // Allow access if authenticated or not restricted
        next();
    }
});

export default router;
