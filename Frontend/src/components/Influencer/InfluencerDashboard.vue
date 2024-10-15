<!-- InfluencerDashboard.vue -->
<template>
  <div class="out">
    <div class="row">
      <div class="col c1">
        <div v-if="influencer" class="container outline">
          <img src="../../assets/profile.jpg" alt=""><br><br>
          <h3>Welcome {{ influencer.username }}</h3><br>
          <p><strong>Category:</strong> {{ influencer.category }}</p>
          <p><strong>Niche:</strong> {{ influencer.niche }}</p>
          <p><strong>Reach:</strong> {{ influencer.reach }}</p>
        </div>
        <div v-else class="container outline">
          <p>Loading influencer details...</p>
        </div>
      </div>
      <div class="col">
        <div class="container right">
          <h4>New Ad Requests:</h4>
          <div v-if="adRequests.length">
            <div class="vstack vs" v-for="ad in adRequests" :key="ad.ad_id">
              <div class="p-2 head">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ ad.sponsor_name }}</div>
                </div>
              </div>
              <div class="p-2">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Message: </strong>{{ ad.messages }}</div>
                  <div class="p-2 ms-auto"><strong>Requirements: </strong>{{ ad.requirements }}</div>
                  <!-- Pass the current ad to the method -->
                  <div class="p-2 ms-auto warn" v-if="isModificationRejected(ad)"><strong>(Requested Payroll Rejected)</strong></div>
                </div>
              </div>
              <div class="p-2 foot">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Payroll: </strong>{{ ad.payroll }}</div>
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-success action" @click.prevent="updateAdStatus(ad.ad_id, 'accept')">Accept</a>
                  </div>
                  <div class="p-2 ms-auto">
                    <router-link :to="{ name: 'ModifyPayroll', params: { ad_id: ad.ad_id } }" class="btn btn-warning action">Negotiate</router-link>
                  </div>
                  <div class="p-2 ms-auto">
                    <a href="" class="btn btn-danger action" @click.prevent="updateAdStatus(ad.ad_id, 'reject')">Reject</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p>No pending ad requests.</p>
          </div>
        </div>
        <br>
        <div class="container right">
          <h4>Active Advertisements:</h4>
          <div v-if="activeAds.length">
            <div class="vstack vsa" v-for="ad in activeAds" :key="ad.ad_id">
              <div class="p-2 heada">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ ad.sponsor_name }}</div>
                </div>
              </div>
              <div class="p-2 foota">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Message: </strong>{{ ad.messages }}</div>
                  <div class="p-2 ms-auto"><strong>Requirements: </strong>{{ ad.requirements }}</div>
                  <div class="p-2 ms-auto"><strong>Payroll: </strong> {{ ad.payroll }}</div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p>No active advertisements currently.</p>
          </div>
        </div>
        <br>
        <div class="container right">
          <div v-if="requestedAds.length">
            <h4>Requested for Ad Collaboration:</h4>
            <div class="vstack vsac" v-for="ad in requestedAds" :key="ad.ad_id">
              <div class="p-2 headac">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ ad.sponsor_name }}</div>
                </div>
              </div>
              <div class="p-2 footac">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Message: </strong>{{ ad.messages }}</div>
                  <div class="p-2 ms-auto"><strong>Requirements: </strong>{{ ad.requirements }}</div>
                  <div class="p-2 ms-auto"><strong>Payroll: </strong> {{ ad.payroll }}</div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p></p>
          </div>
        </div>
        <br>
        <div class="container right">
          <div v-if="modifiedAds.length">
            <h4>Requested Modifications:</h4>
            <div class="vstack vsm" v-for="ad in modifiedAds" :key="ad.ad_id">
              <div class="p-2 headm">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ ad.sponsor_name }}</div>
                </div>
              </div>
              <div class="p-2 footm">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Payroll: </strong>{{ ad.payroll }}</div>
                  <div class="p-2 ms-auto change1">
                    <strong>Requested Payroll: </strong> {{ ad.modified_payroll }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p></p>
          </div>
        </div>
        <br>
        <div class="container right last">
          <div v-if="rejectedAds.length">
            <h4>Rejected Ad Requests:</h4>
            <div class="vstack vsr" v-for="ad in rejectedAds" :key="ad.ad_id">
              <div class="p-2 headr">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Ad Name: </strong>{{ ad.ad_name }}</div>
                  <div class="p-2 ms-auto"><strong>Campaign Name: </strong>{{ ad.camp_name }}</div>
                  <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ ad.sponsor_name }}</div>
                </div>
              </div>
              <div class="p-2 footr">
                <div class="hstack gap-3">
                  <div class="p-2"><strong>Message: </strong>{{ ad.messages }}</div>
                  <div class="p-2 ms-auto"><strong>Requirements: </strong>{{ ad.requirements }}</div>
                  <div class="p-2 ms-auto"><strong>Payroll: </strong> {{ ad.payroll }}</div>
                  <div class="p-2 ms-auto warn" v-if="isRequestedRejected(ad)"><strong>(Rejected by Organization)</strong></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p></p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <InfluencerNav />
  <div class="full" v-if="isFlagged(influencer)">
      <h5 style="color: red;">You have been flagged for violating App Policy!</h5>
      <p>Please contact the admin for further validation.</p><br>
      <a class="btn btn-danger" @click="logout0">Logout</a>
    </div>
</template>



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
.out{
  position: absolute;
  top: 12%;
  left: 10%;
}
.warn{
  color: white;
  background-color: rgb(255, 100, 100);
  border-radius: 5px;
}
.change1{
  background-color: rgb(206, 255, 154);
  border-radius: 5px;
}
.outline{
  margin-top: 15%;
  text-align: center;
  border: solid 5px lightblue;
  padding: 60px 30px;
  border-radius: 20px;
}
.outline img{
  width: 150px;
}
.outline p{
  font-size: 20px;
}
.right{
  margin-left: 10%;
  width: 850px;
  margin-top: 3%;
}
.vs{
  border: 4px solid rgb(136, 227, 255);
  border-radius: 10px;
  text-align: center;
}
.head{
  background-color: rgb(136, 227, 255);
}
.foot{
  border-top: 2px solid rgb(136, 227, 255);
}
.action{
  width: 150px;
}
.vsa{
  border: 4px solid rgb(207, 243, 183);
  border-radius: 10px;
  text-align: center;
}
.heada{
  background-color: rgb(207, 243, 183);
}
.foota{
  border-top: 2px solid rgb(207, 243, 183);
}
.vsac{
  border: 4px solid rgb(246, 216, 255);
  border-radius: 10px;
  text-align: center;
}
.headac{
  background-color: rgb(246, 216, 255);
}
.footac{
  border-top: 2px solid rgb(246, 216, 255);
}
.vsm{
  border: 4px solid rgb(255, 235, 105);
  border-radius: 10px;
  text-align: center;
}
.headm{
  background-color: rgb(255, 235, 105);
}
.footm{
  border-top: 2px solid rgb(255, 235, 105);
}
.vsr{
  border: 4px solid rgb(243, 183, 192);
  border-radius: 10px;
  text-align: center;
}
.headr{
  background-color: rgb(243, 183, 192);
}
.footr{
  border-top: 2px solid rgb(243, 183, 192);
}
.last{
  margin-bottom: 40px;
}
</style>

<script>
import axios from 'axios';
import InfluencerNav from './InfluencerNav.vue';

export default {
  name: 'InfluencerDashboard',
  components: {
    InfluencerNav
  },
  data() {
    return {
      influencer: null,
      adRequests: [],  // Data property for ad requests
      modifiedAds: [],
      activeAds: [],
      rejectedAds: [],
      requestedAds: []
    };
  },
  async created() {
    await this.fetchInfluencerDetails();
    await this.fetchPendingAdRequests();  // Fetch pending ad requests after influencer details
    await this.fetchModifiedAdRequests();
    await this.fetchRejectedAdRequests();
    await this.fetchActiveAds();
    await this.fetchRequestedAds();
  },
  methods: {
    isFlagged(influencer) {
      return influencer.flag === 'flag';
    },
    /**
     * Fetch influencer details from the backend.
     */
    async fetchInfluencerDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/influencer-details', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.influencer = response.data.data;
          // Store influencer ID in localStorage for further use
          localStorage.setItem('influencer_id', this.influencer.inf_id);
        } else {
          console.error('Error loading influencer details:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },

    /**
     * Fetch pending ad requests for the influencer.
     */
    async fetchPendingAdRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/influencer/pending-ad-requests', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.adRequests = response.data.ad_requests;
        } else {
          console.error('Error loading ad requests:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },

    /**
     * Fetch modified ad requests for the influencer.
     */
    async fetchModifiedAdRequests(){
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/influencer/modified-ad-requests', {
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

    async fetchRejectedAdRequests(){
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/influencer/rejected-ad-requests', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.rejectedAds = response.data.rejected_ads;
        } else {
          console.error('Error loading ad requests:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },

    /**
     * Fetch active ads for the influencer.
     */
    async fetchActiveAds(){
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/influencer/active-ads', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.activeAds = response.data.active_ads;
        } else {
          console.error('Error loading ad requests:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },



    /**
     * Fetch requested ad collabs for the influencer.
     */
     async fetchRequestedAds(){
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/influencer/requested-ads', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.requestedAds = response.data.requested_requests;
        } else {
          console.error('Error loading ad requests:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    },

    /**
     * Update the status of an ad request (accept or reject).
     * @param {Number} ad_id - The ID of the ad request.
     * @param {String} action - The action to perform ('accept' or 'reject').
     */
    async updateAdStatus(ad_id, action) {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/api/influencer/ad-request/${ad_id}/update`, {
          action: action
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          // Remove the ad request from the list if status is not pending anymore
          this.adRequests = this.adRequests.filter(ad => ad.ad_id !== ad_id);

          // Optionally, show a success message
          alert(`Ad request has been ${action}ed successfully.`);
          await this.fetchPendingAdRequests();  // Fetch pending ad requests after influencer details
          await this.fetchModifiedAdRequests();
          await this.fetchRejectedAdRequests();
          await this.fetchActiveAds();
          await this.fetchRequestedAds();
        } else {
          // Handle failure
          alert(`Failed to ${action} the ad request: ${response.data.message}`);
        }
      } catch (error) {
        console.error('API Error:', error);
        alert(`An error occurred while trying to ${action} the ad request.`);
      }
    },

    /**
     * Check if an ad modification is rejected.
     * @param {Object} ad - The ad object to check.
     * @returns {Boolean} - Returns true if rejected, else false.
     */
    isModificationRejected(ad) {
      return ad && ad.ad_status === 'pending' && ad.modified_payroll === -1;
    },
    isRequestedRejected(ad) {
      return ad && ad.ad_status === 'rejected' && ad.modified_payroll === -1;
    },
    logout0() {
        localStorage.removeItem('access_token');
        this.$router.push('/user-login');
        window.alert('You are logged out.');
    }
  }
};
</script>
