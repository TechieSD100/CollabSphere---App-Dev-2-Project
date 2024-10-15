<!-- EditCampaign.vue -->
<template>
    <div class="cform">
      <div class="container">
        <div class="row" align="right">
          <div class="col-9">
            <h4>Edit Existing Campaign</h4>
          </div>
          <div class="col-3">
            <router-link :to="`/sponsor-campaigns/${sponsorId}`" class="btn btn-danger">X</router-link>
          </div>
        </div><br>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="campaignName" class="form-label">Campaign Name</label></div>
              <div class="col-7"><input type="text" class="form-control" id="campaignName" v-model="campaignName" required /></div>
            </div>
          </div>
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="campaignDescription" class="form-label">Campaign Description</label></div>
              <div class="col-7"><textarea class="form-control" id="campaignDescription" v-model="campaignDescription"></textarea></div>
            </div> 
          </div>
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="days" class="form-label">No. of Days</label></div>
              <div class="col-7"><input type="number" class="form-control" id="days" v-model="days" required /></div>
            </div>
          </div>
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="budget" class="form-label">Budget</label></div>
              <div class="col-7"><input type="number" class="form-control" id="budget" v-model="budget" required /></div>
            </div>
          </div>
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="visibility" class="form-label">Visibility</label></div>
              <div class="col-7">
                <select class="form-select" aria-label="Default select example" v-model="visibility" required>
                  <option value="public">Public</option>
                  <option value="private">Private</option>
                </select>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <div class="row">
              <div class="col-5"><label for="goals" class="form-label">Goals</label></div>
              <div class="col-7"><input type="text" class="form-control" id="goals" v-model="goals" /></div>
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
    name: 'EditCampaign',
    components: {
      SponsorNav
    },
    data() {
      return {
        sponsorId: this.$route.params.sponsor_id,
        camp_id: this.$route.params.campaign_id,
        campaignName: '',
        campaignDescription: '',
        days: '',
        budget: '',
        visibility: '',
        goals: '',
      };
    },
    async created() {
      await this.fetchCampaignDetails();
    },
    methods: {
        async fetchCampaignDetails() {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/api/edit-campaign/${this.camp_id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        console.log(response.data); // Log the entire response

        if (response.data.status === 'success') {
            const campaign = response.data.data;
            this.campaignName = campaign.camp_name;
            this.campaignDescription = campaign.camp_description;
            this.days = (new Date(campaign.end_date) - new Date(campaign.start_date)) / (1000 * 60 * 60 * 24);
            this.budget = campaign.budget;
            this.visibility = campaign.visibility;
            this.goals = campaign.goals;
            console.log(this.campaignName, this.campaignDescription, this.days, this.budget, this.visibility, this.goals); // Log the values
        } else {
            console.error('Error fetching campaign details:', response.data.message);
        }
    } catch (error) {
        console.error('API Error:', error);
    }
},
      async handleSubmit() {
        try {
          const response = await axios.put(`http://127.0.0.1:5000/api/edit-campaign/${this.camp_id}`, {
            camp_name: this.campaignName,
            camp_description: this.campaignDescription,
            start_date: new Date(Date.now()).toISOString().split('T')[0], // You can change this if needed
            end_date: new Date(Date.now() + this.days * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            budget: this.budget,
            visibility: this.visibility,
            goals: this.goals,
          }, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          });
  
          if (response.data.status === 'success') {
            alert('Campaign updated successfully!');
            this.$router.push(`/sponsor-campaigns/${this.sponsorId}`);
          } else {
            console.error('Error updating campaign:', response.data.message);
          }
        } catch (error) {
          console.error('API Error:', error);
        }
      }
    }
  }
  </script>
  