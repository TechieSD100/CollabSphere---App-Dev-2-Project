<template>
    <div class="cform">
      <div class="container">
        <div class="row" align="right">
            <div class="col-9">
              <h4>Request for Payroll Modification:</h4>
            </div>
            <div class="col-3">
                <router-link :to="{ name: 'InfluencerDashboard', params: { inf_id: influencerId } }" class="btn btn-close"></router-link>
            </div>
        </div><br>
        
        <div v-if="adRequest">
            <div class="ad-details">
                <!-- <p><strong>Ad ID:</strong> {{ adRequest.ad_id }}</p> -->
                <p><strong>Ad Name:</strong> {{ adRequest.ad_name }}</p>
            </div>
            <form @submit.prevent="submitModification">
                <div class="mb-3">
                    <label for="m_payroll" class="form-label">Set Modified Payroll:</label>
                    <input type="number" class="form-control" id="m_payroll" v-model="m_payroll" required min="0">
                </div>
                <div class="d-flex justify-content-center">
                  <button type="submit" class="btn btn-warning">Submit</button>
                </div>
            </form>
        </div>
        <div v-else>
            <p>Loading ad request details...</p>
        </div>
        
      </div>
    </div>
    <InfluencerNav />
</template>

<style scoped>
.ad-details {
    background-color: #f8f9fa;
    padding: 20px;
    padding-bottom: 8px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>

<script>
import axios from 'axios';
import InfluencerNav from './InfluencerNav.vue';

export default {
  name: 'ModifyPayroll',
  components: {
    InfluencerNav
  },
  data(){
    return {
      ad_id: this.$route.params.ad_id,
      adRequest: null,
      m_payroll: '',
      influencerId: localStorage.getItem('influencer_id'), // Added influencerId
    }
  },
  async created(){
    await this.fetchAdRequestDetails();
  },
  methods: {
    async fetchAdRequestDetails(){
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/adrequest/${this.ad_id}/modify-payroll`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.adRequest = response.data.ad_request;
          // Optionally, pre-fill the current payroll
          this.m_payroll = this.adRequest.payroll;
        } else {
          console.error('Error fetching ad request details:', response.data.message);
          alert('Failed to load ad request details.');
          this.$router.push({ name: 'InfluencerDashboard', params: { inf_id: this.influencerId } });
        }
      } catch (error) {
        console.error('API Error:', error);
        alert('An error occurred while fetching ad request details.');
        this.$router.push({ name: 'InfluencerDashboard', params: { inf_id: this.influencerId } });
      }
    },
    async submitModification(){
      if(this.m_payroll < 0){
        alert('Payroll cannot be negative.');
        return;
      }
      try {
        const response = await axios.post(`http://127.0.0.1:5000/api/adrequest/${this.ad_id}/modify-payroll`, {
          modified_payroll: this.m_payroll
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          alert('Payroll modification submitted successfully.');
          this.$router.push({ name: 'InfluencerDashboard', params: { inf_id: this.influencerId } });
        } else {
          alert(`Failed to modify payroll: ${response.data.message}`);
        }
      } catch (error) {
        console.error('API Error:', error);
        alert('An error occurred while submitting the payroll modification.');
      }
    }
  }
};
</script>
