<!-- CreateAd.vue -->
<template>
  <div class="cform">
    <div class="container">
      <div class="row" align="right">
        <div class="col-9">
          <h4>Create New Ad</h4>
        </div>
        <div class="col-3">
          <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${camp_id}`" class="btn btn-close"></router-link>
        </div>
      </div><br>
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <div class="row">
            <div class="col-5"><label for="adName" class="form-label">Ad Name</label></div>
            <div class="col-7"><input type="text" class="form-control" id="adName" v-model="adName" required /></div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <div class="col-5"><label for="adMessage" class="form-label" style="font-size: 15px;">Message</label></div>
            <div class="col-7"><textarea class="form-control" id="adMessage" v-model="adMessage"></textarea></div>
          </div> 
        </div>
        <div class="mb-3">
          <div class="row">
            <div class="col-5"><label for="requirements" class="form-label">Requirements</label></div>
            <div class="col-7"><input type="text" class="form-control" id="requirements" v-model="requirements" /></div>
          </div>
        </div>
        
        <div class="mb-3">
          <div class="row">
            <div class="col-5"><label for="req_influencer" class="form-label">Influencer</label></div>
            <div class="col-7">
              <select class="form-select" aria-label="Default select example" id="req_influencer" v-model="req_influencer" required>
                <option value="0" selected>Yet to be decided</option>
                <option v-for="influencer in influencers" :key="influencer.inf_id" :value="`${influencer.inf_id}`">{{ influencer.username }} - ({{ influencer.category }} | {{ influencer.niche }} | Reach:{{ influencer.reach }})</option>
              </select>
            </div>
          </div>
        </div>
        <div class="mb-3">
          <div class="row">
            <div class="col-5"><label for="payroll" class="form-label">Payroll</label></div>
            <div class="col-7">
              <input type="number" class="form-control" id="payroll" v-model="payroll" />
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <button type="submit" class="btn btn-warning">Submit</button>
        </div>
      </form>
    </div>
  </div>
  <SponsorNav/>
</template>



<script>
import SponsorNav from './SponsorNav.vue';
import axios from 'axios';

export default {
  name: 'CreateAd',
  components: {
    SponsorNav
  },
  data() {
    return {
      adName: '',
      adMessage: '',
      requirements: '',
      req_influencer: '',
      payroll: 0,
      influencers: [],
      sponsorId: localStorage.getItem('sponsor_id'),
      camp_id: this.$route.params.campaign_id,
      campaignBudget: 0, // to store the budget fetched from the backend
    };
  },
  created() {
    this.fetchInfluencers();
    this.fetchCampaignDetails();
  },
  methods: {
    async fetchInfluencers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/fetch-influencers', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
        this.influencers = response.data.inf_data;
      } catch (error) {
        console.error('Error fetching influencers:', error);
      }
    },
    async fetchCampaignDetails() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/campaign-details/${this.camp_id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
        this.campaignBudget = response.data.budget;
      } catch (error) {
        console.error('Error fetching campaign details:', error);
      }
    },
    async handleSubmit() {
  try {
    const payload = {
      sponsor_id: this.sponsorId,
      camp_id: this.$route.params.campaign_id,
      inf_id: this.req_influencer,
      ad_name: this.adName,
      ad_message: this.adMessage,
      requirements: this.requirements,
      payroll: this.payroll
    };

    const response = await axios.post('http://127.0.0.1:5000/api/create-ad', payload, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.data.status === 'success') {
      alert('Ad created successfully!');
      this.$router.push(`/sponsor-campaigns/${this.sponsorId}/campaign-details/${this.camp_id}`);
    } else {
      alert(response.data.message);  // Handle other errors
    }
  } catch (error) {
    // Check if it's a validation error from the backend
    if (error.response && error.response.status === 400) {
      const message = error.response.data.message;

      if (message.includes('Payroll exceeds remaining budget')) {
        const remainingBudget = error.response.data.remaining_budget;
        alert(`You only have a remaining budget of ${remainingBudget}. Please lower the payroll.`);
      }
      // else if (message.includes('Ad with this influencer already exists for this campaign')) {
      //   alert('An ad with this influencer already exists under this campaign. Please select another influencer.');
      // }
      else {
        alert(message);  // Handle other validation errors
      }
    } else {
      console.error('Error submitting the form:', error);
      alert('There was an issue submitting the form. Please try again.');
    }
  }
}

  }
};
</script>
