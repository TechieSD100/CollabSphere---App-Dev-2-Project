<!-- SponsorCampaigns.vue -->
<template>
    <div>
      
      <div v-if="campaigns.length > 0" class="container main1">
        <h4>Your Campaigns</h4>
        
        <div class="row">
          <div class="col" v-for="campaign in campaigns" :key="campaign.camp_id">
            <div class="card">
              <div class="card-body cb1">
                <h5 class="card-title">{{ campaign.camp_name }}</h5>
                <p class="card-text">{{ campaign.camp_description }}</p>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item lgi"><p class="card-text"><strong>Start Date:</strong> {{ campaign.start_date }}</p></li>
                <li class="list-group-item lgi"><p class="card-text"><strong>End Date:</strong> {{ campaign.end_date }}</p></li>
                <li class="list-group-item lgi"><p class="card-text"><strong>Budget:</strong> {{ campaign.budget }}</p></li>
                <li class="list-group-item lgi"><p class="card-text"><strong>Visibility:</strong> {{ campaign.visibility }}</p></li>
                <li class="list-group-item lgi"><p class="card-text"><strong>Goals:</strong> {{ campaign.goals }}</p></li>
              </ul>
              <div class="card-body cb3">
                <button class="btn btn-primary" @click="exportCSV(campaign.camp_id)">Download Report</button>
              </div>
              <div class="card-body cb2">
                <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${campaign.camp_id}`" class="btn btn-success">View</router-link>
                <router-link :to="`/sponsor-campaigns/${sponsorId}/edit-campaign/${campaign.camp_id}`" class="btn btn-warning">Edit</router-link>
                <button @click="deleteCampaign(campaign.camp_id)" class="btn btn-danger">Delete</button>
              </div>    
            </div>
          </div>
        </div>
        <router-link :to="`/sponsor-campaigns/${sponsorId}/add-campaign`" class="click">
            <div class="add">
                <p>Add New Campaign</p>
            </div>
        </router-link>
      </div>
      <div v-else class="container main2">
        <p>You do not have any active campaigns.</p><br>
        <router-link :to="`/sponsor-campaigns/${sponsorId}/add-campaign`" class="click">
            <div class="add">
                <p>Add New Campaign</p>
            </div>
        </router-link>
      </div>
    </div>
    <SponsorNav />
  </template>


<style>
.main1{
  position: absolute;
  left: 7%;
  top: 15%;
  text-align: center;
  /* background-color: lightblue; */
}
.main1 .card{
  margin: 20px;
  width: 18rem;
  margin-left: 50%;
  transform: translateX(-50%);
  border-radius: 25px;
  border: 5px solid rgb(203, 255, 114);
}
.main1 .add{
  margin-left: 50%;
  transform: translateX(-50%);
  width: 400px;
  font-size: 18px;
  background-color: white;
}
.lgi{
  background-color: rgb(203, 255, 114);
}
.card-body .btn{
  margin-left: 10px;
  margin-right: 10px;
}
.main2{
    /* background-color: lightblue; */
    text-align: center;
    margin-left: 50%;
    margin-top: -25%;
}
.main2 p{
    font-size: 18px;
    font-weight: 400;
}
.add{
    border: solid 4px lightgreen;
    border-radius: 15px;
    padding: 20px;
    font-size: 25px;
    padding-bottom: 8px;
}
.cb3{
  border-bottom: 4px solid rgb(203, 255, 114);
}
.click{
    text-decoration: none;
    color: black;
}
</style>


<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'SponsorCampaigns',
  components: {
    SponsorNav
  },
  data() {
    return {
      campaigns: [],
      sponsorId: localStorage.getItem('sponsor_id'), // Fetch the sponsor ID from localStorage
    };
  },
  methods: {
    async exportCSV(camp_id) {
      const response = await axios.get(`http://127.0.0.1:5000/api/trigger/${camp_id}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            })
            .then(response => {
              setTimeout(() => {window.open("http://127.0.0.1:5000/api/download")}, 2000)
            })
            .catch(error => {
              console.error(error);
              window.alert('Failed to export CSV file');
            })
    },
    async deleteCampaign(camp_id) {
        try {
            const response = await axios.delete(`http://127.0.0.1:5000/api/sponsor-campaigns/${camp_id}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.data.status === 'success') {
                // Remove the deleted campaign from the campaigns array
                this.campaigns = this.campaigns.filter(campaign => campaign.camp_id !== camp_id);
                alert(response.data.message);
            } else {
                console.error('Error deleting campaign:', response.data.message);
            }
        } catch (error) {
            console.error('API Error:', error);
        }
    }
  },
  async created() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/sponsor-campaigns', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });

      if (response.data.status === 'success') {
        this.campaigns = response.data.data;
      } else {
        console.error('Error loading campaigns:', response.data.message);
      }
    } catch (error) {
      console.error('API Error:', error);
    }
  }
};
</script>