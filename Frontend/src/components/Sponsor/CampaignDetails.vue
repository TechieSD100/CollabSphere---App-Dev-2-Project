<!-- CampaignDetails.vue -->

<template>
  <div class="container out">
    <div class="container cdetails">
      <div class="row" align="center">
        <div class="col">
          <h4><strong>{{ campaign.camp_name }}</strong></h4>
        </div>
        <div class="col">
          <h5><strong>End Date:</strong> {{ campaign.end_date }}</h5>
        </div>
        <div class="col">
          <h5><strong>Total Budget:</strong> {{ campaign.budget }}</h5>
        </div>
        <div class="col">
          <h5>
            <strong>Remaining Budget:</strong> {{ remainingBudget }}
          </h5>
        </div>
      </div>
    </div>

    <div v-if="adRequests.length > 0">
      <div class="addisplay">
        <h4 align="center"><strong>Ad Requests</strong></h4><br>
        <div class="row">
          <div class="col-4" v-for="request in adRequests" :key="request.id" style="margin-bottom: 35px;">
            <div class="card cw">
              <div class="card-body cbtop">
                <h5 class="card-title"><strong>{{ request.ad_title }}</strong></h5>
                <p class="card-text"><strong>Status:</strong> {{ request.status }}</p>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><p class="card-text"><strong>Influencer: </strong>{{ request.inf_name }}</p></li>
                <li class="list-group-item"><p class="card-text"><strong>Message:</strong> {{ request.ad_message }}</p></li>
                <li class="list-group-item"><p class="card-text"><strong>Requirements:</strong> {{ request.requirements }}</p></li>
                <li class="list-group-item"><p class="card-text"><strong>Payroll:</strong> {{ request.payroll }}</p></li>
              </ul>
              <div class="card-body">
                <div class="row">
                  <div class="col" align="center" v-if="isNotRejectedOrAccepted(request)">
                    <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${campaign.camp_id}/edit-ad/${request.ad_id}`" class="btn btn-warning" style="width: 100px;">Edit</router-link>
                  </div>
                  <div class="col" align="center">
                    <button @click="deleteAdRequest(request.ad_id)" class="btn btn-danger" style="width: 100px;">Delete</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${campaign.camp_id}/create-ad`" class="click">
        <div class="add">
          <p>Create New Ad</p>
        </div>
      </router-link>
    </div>

    <div class="noad" v-else>
      <p>No ad requests for this campaign.</p>
      <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${campaign.camp_id}/create-ad`" class="click">
        <div class="add">
          <p>Create New Ad</p>
        </div>
      </router-link>
    </div>
  </div>
  <SponsorNav />
</template>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'CampaignDetails',
  components: {
    SponsorNav,
  },
  props: ['sponsorId', 'campaignId'],
  data() {
    return {
      campaign: {},
      adRequests: [],
      sponsorId: localStorage.getItem('sponsor_id')
    };
  },
  computed: {
    remainingBudget() {
      // Calculate remaining budget
      return this.campaign.budget - this.campaign.total_payroll;
    }
  },
  methods: {
    isNotRejectedOrAccepted(ad){
      return ad.status !== 'rejected' && ad.status !== 'accepted';
    },
    async loadCampaignDetails() {
      const campaignId = this.$route.params.campaign_id;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/campaign-details/${campaignId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        if (response.data.status === 'success') {
          this.campaign = response.data.data;
          this.adRequests = response.data.data.ad_requests || []; // Load ad requests
        } else {
          console.error('Error loading campaign details:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },
    
    async deleteAdRequest(adId) {
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/api/delete-ad/${adId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });
        if (response.data.status === 'success') {
          this.adRequests = this.adRequests.filter(request => request.id !== adId);
          
          // Reload the campaign details after deletion
          this.loadCampaignDetails();
          alert(response.data.message);

        } else {
          console.error('Error deleting ad:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    }
  },
  created() {
    this.loadCampaignDetails();
  }
};
</script>

<style scoped>
.out {
  position: absolute;
  left: 7%;
  top: 11%;
}
.cdetails{
  border: solid 2px rgb(255, 204, 0);
  border-radius: 20px;
  padding: 20px;
  padding-top: 30px;
  margin-bottom: 30px;
}
.noad{
  text-align: center;
}
.add{
  text-align: center;
  width: 350px;
  margin-left: 50%;
  transform: translateX(-50%);
}
.cw{
  width: 90%;
  border: 5px solid rgb(255, 201, 230);
  border-radius: 20px;
}
.cbtop{
  text-align: center;
  background-color: rgb(255, 201, 230);
}
.addisplay{
  margin-bottom: 20px;
}
</style>
