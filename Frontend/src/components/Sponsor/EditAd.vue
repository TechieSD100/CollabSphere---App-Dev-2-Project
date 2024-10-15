<!-- EditAd.vue -->

<template>
    <div class="cform">
        <div class="container">
            <!-- Header with Close Button -->
            <div class="row" align="right">
                <div class="col-9">
                    <h4>Edit Existing Ad</h4>
                </div>
                <div class="col-3">
                    <!-- Close Button Redirects to Campaign Details -->
                    <router-link :to="`/sponsor-campaigns/${sponsorId}/campaign-details/${camp_id}`" class="btn btn-close"></router-link>
                </div>
            </div>
            <br>
            
            <!-- Edit Ad Form -->
            <form @submit.prevent="handleSubmit">
                <!-- Ad Name -->
                <div class="mb-3">
                    <div class="row">
                        <div class="col-5">
                            <label for="adName" class="form-label">Ad Name</label>
                        </div>
                        <div class="col-7">
                            <input type="text" class="form-control" id="adName" v-model="adName" required />
                        </div>
                    </div>
                </div>
                
                <!-- Message -->
                <div class="mb-3">
                    <div class="row">
                        <div class="col-5">
                            <label for="adMessage" class="form-label" style="font-size: 15px;">Message</label>
                        </div>
                        <div class="col-7">
                            <textarea class="form-control" id="adMessage" v-model="adMessage"></textarea>
                        </div>
                    </div> 
                </div>
                
                <!-- Requirements -->
                <div class="mb-3">
                    <div class="row">
                        <div class="col-5">
                            <label for="requirements" class="form-label">Requirements</label>
                        </div>
                        <div class="col-7">
                            <input type="text" class="form-control" id="requirements" v-model="requirements" />
                        </div>
                    </div>
                </div>
                
                <!-- Influencer Selection -->
                <div class="mb-3">
                    <div class="row">
                        <div class="col-5">
                            <label for="req_influencer" class="form-label">Influencer</label>
                        </div>
                        <div class="col-7">
                            <select class="form-select" aria-label="Select Influencer" id="req_influencer" v-model="req_influencer" required>
                                <option value="0">Yet to be decided</option>
                                <option v-for="influencer in influencers" :key="influencer.inf_id" :value="influencer.inf_id">
                                    {{ influencer.username }} - ({{ influencer.category }} | {{ influencer.niche }} | Reach: {{ influencer.reach }})
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Payroll -->
                <div class="mb-3">
                    <div class="row">
                        <div class="col-5">
                            <label for="payroll" class="form-label">Payroll</label>
                        </div>
                        <div class="col-7">
                            <input type="number" class="form-control" id="payroll" v-model="payroll" required />
                        </div>
                    </div>
                </div>
                
                <!-- Error Message -->
                <div v-if="error" class="alert alert-danger" role="alert">
                    {{ error }}
                </div>
                
                <!-- Submit Button -->
                <div class="d-flex justify-content-center">
                    <button type="submit" class="btn btn-warning" :disabled="isSubmitting">
                        <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span v-else>Submit</span>
                    </button>
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
    name: 'EditAd',
    components: {
        SponsorNav
    },
    data() {
        return {
            sponsorId: this.$route.params.sponsor_id,
            camp_id: this.$route.params.campaign_id,
            ad_id: this.$route.params.ad_id, // Extract ad_id from route params
            adName: '',
            adMessage: '',
            requirements: '',
            payroll: '',
            req_influencer: 0, // 0 represents "Yet to be decided"
            influencers: [], // List of influencers for the dropdown
            error: '',
            isSubmitting: false
        }
    },
    methods: {
        /**
         * Fetch existing AdRequest data for editing.
         */
        async fetchAdRequestData() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/ad-request/${this.ad_id}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                });
                if (response.data.status === 'success') {
                    const adData = response.data.data;
                    this.adName = adData.ad_name;
                    this.adMessage = adData.ad_message;
                    this.requirements = adData.requirements;
                    this.payroll = adData.payroll;
                    this.req_influencer = adData.inf_id ? adData.inf_id : 0;
                    this.influencers = adData.influencers;
                } else {
                    this.error = response.data.message || 'Failed to load ad data.';
                }
            } catch (error) {
                console.error('Error fetching ad data:', error);
                this.error = 'Error fetching ad data.';
            }
        },
        /**
         * Handle form submission to update AdRequest.
         */
        async handleSubmit() {
            this.error = '';
            this.isSubmitting = true;
            try {
                const payload = {
                    ad_name: this.adName,
                    ad_message: this.adMessage,
                    requirements: this.requirements,
                    payroll: this.payroll,
                    inf_id: this.req_influencer
                };
                const response = await axios.put(`http://127.0.0.1:5000/api/ad-request/${this.ad_id}`, payload, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                });
                if (response.data.status === 'success') {
                    alert('Ad request updated successfully.');
                    // Redirect to campaign details page
                    this.$router.push(`/sponsor-campaigns/${this.sponsorId}/campaign-details/${this.camp_id}`);
                } else {
                    this.error = response.data.message || 'Failed to update ad request.';
                }
            } catch (error) {
                console.error('Error updating ad request:', error);
                if (error.response && error.response.data && error.response.data.message) {
                    this.error = error.response.data.message;
                } else {
                    this.error = 'An unexpected error occurred while updating the ad request.';
                }
            } finally {
                this.isSubmitting = false;
            }
        }
    },
    created() {
        this.fetchAdRequestData();
    }
}
</script> 

