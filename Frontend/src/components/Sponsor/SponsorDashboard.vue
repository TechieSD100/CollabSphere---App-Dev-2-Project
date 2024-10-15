<!-- SponsorDashboard.vue -->

<template>
    <div class="container p1" v-if="sponsor">
      <h2 style="margin-bottom: 30px;">Welcome {{ sponsor.org_name }}</h2>


      <div v-if="requestedAds.length">
              <h4>New Ad Collaboration Requests:</h4>
            <div class="vstack vsr" v-for="ad in requestedAds" :key="ad.ad_id">
              <div class="p-2 headr">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-success action" @click.prevent="updateReqAdStatus(ad.ad_id, 'accept')">Accept</a>
                  </div>
                </div>
              </div>
              <div class="p-2 footr">
                <div class="hstack gap-3">
                  <div class="p-2 highlight"><strong>From Influencer: </strong>{{ ad.username }}</div>
                  <div class="p-2 ms-auto"><strong>Payroll: </strong>{{ ad.payroll }}</div>
                  <!-- <div class="p-2 ms-auto" style="background-color: lightseagreen; color: white; border-radius: 5px;"><strong>Requested Payroll: </strong> {{ ad.modified_payroll }}</div> -->
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-danger action" @click.prevent="updateReqAdStatus(ad.ad_id, 'reject')">Reject</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p></p>
          </div>
          <br><br>


      <div v-if="modifiedAds.length">
              <h4>Requested Modifications:</h4>
            <div class="vstack vsm" v-for="ad in modifiedAds" :key="ad.ad_id">
              <div class="p-2 headm">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Influencer: </strong>{{ ad.username }}</div>
                </div>
              </div>
              <div class="p-2 footm">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Assigned Payroll: </strong>{{ ad.payroll }}</div>
                  <div class="p-2 ms-auto" style="background-color: lightseagreen; color: white; border-radius: 5px;"><strong>Requested Payroll: </strong> {{ ad.modified_payroll }}</div>
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-success action" @click.prevent="updateAdStatus(ad.ad_id, 'accept')">Accept</a>
                  </div>
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-danger action" @click.prevent="updateAdStatus(ad.ad_id, 'reject')">Reject</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p></p>
          </div>
          <br><br>
      <div v-if="sponsor.campaigns.length">
        <h4>Your Campaigns:</h4>
        <div class="vstack gap-3">
            <div class="hstack hs gap-3" align="left" v-for="campaign in sponsor.campaigns" :key="campaign.camp_id">
              <div class="p-2"><strong>{{ campaign.camp_name }}</strong></div>
              <div class="p-2 ms-auto">Budget: {{ campaign.budget }}</div>
              <div class="p-2 ms-auto">Status: {{ campaign.status }}</div>
              <div class="p-2 ms-auto">Budget Used: {{ campaign.budget_used_percentage }}%</div>
              <div class="p-2 ms-auto">Day Progress: {{ campaign.day_progress_percentage }}%</div>
              <div class="p-2 ms-auto"><router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${campaign.camp_id}`" class="btn btn-info">View</router-link></div>
            </div>
        </div>
      </div>
      <div v-else>
        <p><strong>No campaigns created yet.</strong><br>Go to 'My Campaigns' to create a new campaign.</p>
      </div>
      <br>
    </div>
    <div v-else>
      <div class="row">
        <div class="col-10"><p>Loading sponsor details...</p></div>
        <div class="col-2">
          <div class="spinner-border text-warning" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>
    <SponsorNav />
    <!-- If Sponsor Signup is yet to be accepted -->
    <div class="full" v-if="isPendingSignup">
      <h5 style="color: orange;">Oops! Your SignUp Request is still Pending!</h5>
      <p>Please wait for the admin to approve your request.</p><br>
      <a class="btn btn-danger" @click="logout0">Logout</a>
    </div>
    <!-- If Sponsor Signup gets declined -->
    <div class="full" v-if="isDeclinedSignup">
      <h5 style="color: red;">Sorry! Your signup request has been declined.</h5>
      <p>Please contact the admin to seek for validity.</p><br>
      <a class="btn btn-danger" @click="logout0">Logout</a>
    </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nerko+One&family=Playpen+Sans:wght@100..800&display=swap');
</style>
<style scoped>
.full{
  position: absolute;
  background-color: white;
  width: 100%;
  height: 100%;
  left: 0%;
  top: 0%;
  text-align: center;
}
.full h5{
  margin-top: 18%;
}
.hs{
  width: 1000px;
  background-color: rgb(200, 241, 255);
  border: 3px solid rgb(77, 195, 255);
  border-radius: 20px;
  padding: 20px 40px;
}
.p1 {
  position: absolute;
  left: 5%;
  top: 12%;
}
.p1 h2{
  font-family: "Playpen Sans", cursive;
  font-optical-sizing: auto;
  font-weight: 600;
  font-style: normal;
}
.vsr{
border: 4px solid rgb(205, 255, 105);
border-radius: 10px;
text-align: center;
width: 1000px;
}
.headr{
background-color: rgb(205, 255, 105);
}
.footr{
border-top: 2px solid rgb(205, 255, 105);
}
.vsm{
border: 4px solid rgb(255, 235, 105);
border-radius: 10px;
text-align: center;
width: 1000px;
}
.headm{
background-color: rgb(255, 235, 105);
}
.footm{
border-top: 2px solid rgb(255, 235, 105);
}
.action{
  width: 150px;
}
.highlight{
  background-color: rgb(255, 255, 168);
  border-radius: 5px;
}
</style>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'SponsorDashboard',
  components: {
    SponsorNav
  },
  data() {
    return {
      sponsor: null,
      modifiedAds: [],
      requestedAds: [],
      sponsorId: localStorage.getItem('sponsor_id')
    };
  },
  computed: {
    // Computed property to check if the sponsor's signup is pending
    isPendingSignup() {
      return this.sponsor && this.sponsor.budget === 0;
    },
    isDeclinedSignup() {
      return this.sponsor && this.sponsor.budget === 2;
    }
  },
  async created() {
    await this.sponsorDetails();
    await this.fetchModifiedRequests();
    await this.fetchRequestedRequests();
  },
  
  methods: {
    async sponsorDetails() {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/sponsor-details', {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                this.sponsor = response.data.data;
                // Store sponsor ID in localStorage for further use
                localStorage.setItem('sponsor_id', this.sponsor.sponsor_id);
            } else {
                console.error('Error loading sponsor details:', response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
        }
    },
    async fetchModifiedRequests(){
        try{
            const response = await axios.get('http://127.0.0.1:5000/api/sponsor/modified-payroll-requests', {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                this.modifiedAds = response.data.modified_ads;
            } else {
                console.error('Error loading ad requests:', response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
        }
    },
    async fetchRequestedRequests(){
        try{
            const response = await axios.get('http://127.0.0.1:5000/api/sponsor/influencer-requested-requests', {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                this.requestedAds = response.data.requested_ads;
            } else {
                console.error('Error loading ad requests:', response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
        }
    },
    async updateAdStatus(ad_id, action) {
        if (!confirm(`Are you sure you want to ${action} this ad request?`)) {
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/sponsor/update-ad-status', {
                ad_id: ad_id,
                action: action
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                // Optionally, display a success message
                alert(response.data.message);
                // Refresh the modifiedAds list
                this.fetchModifiedRequests();
            } else {
                console.error('Error updating ad status:', response.data.message);
                alert(response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
            alert('An error occurred while updating the ad status.');
        }
    },
    async updateReqAdStatus(ad_id, action) {
        if (!confirm(`Are you sure you want to ${action} this ad request?`)) {
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/sponsor/update-requested-ad-status', {
                ad_id: ad_id,
                action: action
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                // Optionally, display a success message
                alert(response.data.message);
                // Refresh the modifiedAds list
                this.fetchRequestedRequests();
            } else {
                console.error('Error updating ad status:', response.data.message);
                alert(response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
            alert('An error occurred while updating the ad status.');
        }
    },
    logout0() {
        localStorage.removeItem('access_token');
        this.$router.push('/user-login');
        window.alert('You are logged out.');
    }
}

};
</script>
