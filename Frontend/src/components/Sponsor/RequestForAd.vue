<!-- RequestForAd.vue -->


<template>
  <div class="cform cc">
    <div class="container">
      <div class="row" align="right">
        <div class="col-9">
          <h4>Send Ad Request:</h4>
        </div>
        <div class="col-3">
          <router-link :to="`/find-influencer/${sponsorId}/`" class="btn btn-danger">X</router-link>
        </div>
      </div><br>
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <div class="row">
            <div class="col-4"><label for="influencerDetails" class="form-label">To Influencer:</label></div>
            <div class="col-8"><input type="text" class="form-control" id="influencerDetails" v-model="influencerDet" disabled /></div>
          </div>
        </div>
        
        <div class="mb-3">
          <div class="row">
            <div class="col-4"><label for="unassigned_ads" class="form-label">For Ad:</label></div>
            <div class="col-8">
              <select class="form-select" aria-label="Default select example" id="unassigned_ads" v-model="selectedAd" required>
                <option v-for="ad in all_ads" :key="ad.ad_id" :value="ad.ad_id">{{ ad.ad_name + " | Payroll:" + ad.payroll }}</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="d-flex justify-content-center">
          <button type="submit" class="btn btn-warning">Submit</button>
        </div>
      </form>
    </div>
  </div>
  <SponsorNav />
</template>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'RequestForAd',
  components: {
    SponsorNav
  },
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id'),
      camp_id: localStorage.getItem('campaign_id'),
      influencerId: this.$route.params.influencer_id,  // Correct influencerId
      influencerDet: '',
      all_ads: [],
      selectedAd: null
    };
  },
  created(){
    this.influencerDetail();
    this.fetchUnassignedAds();
  }
  ,
  methods: {
    async influencerDetail() {
      localStorage.setItem('influencer_id', this.$route.params.influencer_id);
      try {
        // Fetch the influencer's details using this.influencerId
        const response = await axios.get(`http://127.0.0.1:5000/api/influencer/${this.influencerId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}` // Ensure JWT token is sent
          }
        });
        
        if (response.data.status === 'success') {
          this.influencerDet = response.data.influencer.username + " | " + response.data.influencer.category + " | " + response.data.influencer.niche;
        } 
        else {
          console.error(response.data.message); // Log error message
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    async fetchUnassignedAds(){
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/ads/unassigned/${this.sponsorId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
        this.all_ads = response.data.all_ads;
      } catch (error) {
        console.error('Error fetching unassigned ads:', error);
      }
    },

    // Method to submit the selected Ad and assign the influencer
    async handleSubmit() {
      try {
        // Send the selected ad_id and influencer_id to the backend
        const response = await axios.post('http://127.0.0.1:5000/api/adrequest/update', {
          ad_id: this.selectedAd,
          influencer_id: this.influencerId
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.data.status === 'success') {
          alert('Influencer assigned successfully!');
          this.$router.push(`/sponsor-campaigns/${this.sponsorId}/campaign-details/${this.camp_id}`);
        } else {
          console.error(response.data.message); // Log error message
        }
      } catch (error) {
        console.error('Error updating ad request:', error);
      }
    }
  }
}
</script>

<style>
.cc .container{
  width: 500px;
}
</style>
