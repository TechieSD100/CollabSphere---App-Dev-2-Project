<!-- AddCampaign.vue -->
<template>
  <div class="cform">
    <div class="container">
      <div class="row" align="right">
        <div class="col-9">
          <h4>Add New Campaign</h4>
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
            <div class="col-5"><label for="campaignDescription" class="form-label" style="font-size: 15px;">Campaign Description</label></div>
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
              <select class="form-select" aria-label="Default select example" v-model="visibility"  required>
                <option value="public" selected>Public</option>
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

<style>
.cform {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 171, 0.2);
}

.cform .container {
  border-radius: 20px;
  padding: 35px 30px 35px 30px;
  width: 450px;
  background-color: rgb(255, 245, 169);
  margin: 0;
  position: absolute;
  top: 52%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.cform .container h4 {
  text-align: left;
  padding-top: 5px;
}

.cform .container form {
  padding-top: 10px;
}
.cform .container form button{
  margin-top: 10px;
}
</style>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'AddCampaign',
  components: {
    SponsorNav
  },
  data() {
    return {
      campaignName: '',
      campaignDescription: '',
      days: '',
      budget: '',
      visibility: 'public',
      goals: '',
      sponsorId: localStorage.getItem('sponsor_id')
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/add-campaign', {
          camp_name: this.campaignName,
          camp_description: this.campaignDescription,
          start_date: new Date().toISOString().split('T')[0],  // Use today's date for simplicity
          end_date: this.calculateEndDate(),
          budget: this.budget,
          visibility: this.visibility,
          goals: this.goals,
          sponsor_id: this.sponsorId
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          // Redirect to sponsor campaigns page
          this.$router.push(`/sponsor-campaigns/${this.sponsorId}`);
        } else {
          console.error('Error adding campaign:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },
    calculateEndDate() {
      const startDate = new Date();
      const endDate = new Date(startDate);
      endDate.setDate(startDate.getDate() + parseInt(this.days));
      return endDate.toISOString().split('T')[0];
    }
  }
};
</script>
