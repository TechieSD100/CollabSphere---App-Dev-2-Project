<!-- FindAds.vue -->

<template>
    <div class="container ch">
        <div class="row">
            <div class="col-2"></div>
            <div class="col-2">
                <h4>Find Ads</h4>
            </div>
            <div class="col-6">
                <form class="d-flex" @submit.prevent="searchAds">
                    <input v-model="searchQuery" class="form-control me-2" type="search" placeholder="Search by Ad Name, Campaign Name, or Requirements" aria-label="Search">
                    &nbsp;&nbsp;&nbsp;
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
        <hr>
        <p align="center" style="background-color: lightyellow; padding: 10px; border-radius: 10px; color: green;">Note: Only ads with public campaigns are displayed here.</p>

        <div class="row mt-4" v-if="name_ads.length">
            <h5>Found by Ad Name:</h5>
            <table class="table table-success table-striped">
                <thead>
                    <tr align="center">
                        <th><strong>Ad Name</strong></th>
                        <th><strong>Campaign Name</strong></th>
                        <th><strong>Requirements</strong></th>
                        <th><strong>Message</strong></th>
                        <th><strong>Payroll</strong></th>
                        <th><strong>Request</strong></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in name_ads" :key="ad.ad_id" align="center">
                        <td>{{ ad.ad_name }}</td>
                        <td>{{ ad.camp_name }}</td>
                        <td>{{ ad.requirements }}</td>
                        <td>{{ ad.message }}</td>
                        <td>{{ ad.payroll }}</td>
                        <td><button class="btn btn-warning" @click="requestToJoin(ad.ad_id)">Request to Join</button></td>
                    </tr>
                </tbody>
            </table>
        </div>



        <div class="row mt-4" v-if="camp_ads.length">
            <h5>Found by Campaign Name:</h5>
            <table class="table table-primary table-striped">
                <thead>
                    <tr align="center">
                        <th><strong>Ad Name</strong></th>
                        <th><strong>Campaign Name</strong></th>
                        <th><strong>Requirements</strong></th>
                        <th><strong>Message</strong></th>
                        <th><strong>Payroll</strong></th>
                        <th><strong>Request</strong></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in camp_ads" :key="ad.ad_id" align="center">
                        <td>{{ ad.ad_name }}</td>
                        <td>{{ ad.camp_name }}</td>
                        <td>{{ ad.requirements }}</td>
                        <td>{{ ad.message }}</td>
                        <td>{{ ad.payroll }}</td>
                        <td><button class="btn btn-warning" @click="requestToJoin(ad.ad_id)">Request to Join</button></td>
                    </tr>
                </tbody>
            </table>
        </div>




        <div class="row mt-4" v-if="req_ads.length">
            <h5>Found by Requirements:</h5>
            <table class="table table-danger table-striped">
                <thead>
                    <tr align="center">
                        <th><strong>Ad Name</strong></th>
                        <th><strong>Campaign Name</strong></th>
                        <th><strong>Requirements</strong></th>
                        <th><strong>Message</strong></th>
                        <th><strong>Payroll</strong></th>
                        <th><strong>Request</strong></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in req_ads" :key="ad.ad_id" align="center">
                        <td>{{ ad.ad_name }}</td>
                        <td>{{ ad.camp_name }}</td>
                        <td>{{ ad.requirements }}</td>
                        <td>{{ ad.message }}</td>
                        <td>{{ ad.payroll }}</td>
                        <td><button class="btn btn-warning" @click="requestToJoin(ad.ad_id)">Request to Join</button></td>
                    </tr>
                </tbody>
            </table>
        </div>




        <div class="row mt-4" v-if="all_ads.length && !searched && !name_ads.length && !camp_ads.length && !req_ads.length">
            <h5>All Ads:</h5>
            <table class="table table-info table-striped">
                <thead>
                    <tr align="center">
                        <th><strong>Ad Name</strong></th>
                        <th><strong>Campaign Name</strong></th>
                        <th><strong>Requirements</strong></th>
                        <th><strong>Message</strong></th>
                        <th><strong>Payroll</strong></th>
                        <th><strong>Request</strong></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in all_ads" :key="ad.ad_id" align="center">
                        <td>{{ ad.ad_name }}</td>
                        <td>{{ ad.camp_name }}</td>
                        <td>{{ ad.requirements }}</td>
                        <td>{{ ad.message }}</td>
                        <td>{{ ad.payroll }}</td>
                        <td><button class="btn btn-warning" @click="requestToJoin(ad.ad_id)">Request to Join</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <br>
            <p align="center" style="color: red;" v-if="!searched">No unassigned ads available right now.</p>
        </div>
        <div v-if="searched && !name_ads.length && !camp_ads.length && !req_ads.length">
            <p align="center" style="color: red;">No ads found for "{{ searchQuery }}"</p>
        </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    </div>
    <InfluencerNav/>
</template>

<script>
import axios from 'axios';
import InfluencerNav from './InfluencerNav.vue';

export default{
    name: 'FindAds',
    components: {
        InfluencerNav
    },
    data() {
        return {
            all_ads: [],
            name_ads: [],
            camp_ads: [],
            req_ads: [],
            searchQuery: '',
            searched: false,
            error: ''
        }
    },
    created(){
        this.fetchAllAds();
    }
    ,
    methods: {
        async searchAds(){
            if (this.searchQuery.trim() === '') {
                this.fetchAllAds();
            } else {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/api/ads-search', {
                        params: { query: this.searchQuery },  // Ensure query is passed
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                            'Content-Type': 'application/json'
                        }
                    });
                    this.all_ads = response.data.ads_all;
                    this.name_ads = response.data.ads_name;
                    this.camp_ads = response.data.ads_campaign;
                    this.req_ads = response.data.ads_requirements;
                    this.searched = true;
                } catch (error) {
                    console.error('Error fetching ads:', error);
                    this.error = 'Error fetching ads: ' + error;
                }
            }
        },
        async fetchAllAds() {
            try{
                const response = await axios.get('http://127.0.0.1:5000/api/ads-search', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                });
                this.all_ads = response.data.ads_all;
                this.name_ads = [];
                this.camp_ads = [];
                this.req_ads = [];
                this.searched = false;
            } catch (error){
                console.error('Error fetching all ads:', error);
                this.error = 'Error fetching all ads: ' + error;
            }
        },
        /**
     * Handle the "Request to Join" action.
     * @param {Number} ad_id - The ID of the ad to join.
     */
    async requestToJoin(ad_id) {
        // Optional: Confirm the action with the user
        if (!confirm('Are you sure you want to request to join this ad?')) {
            return;
        }

        try {
            const response = await axios.post(`http://127.0.0.1:5000/api/ads/${ad_id}/join`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data.status === 'success') {
                alert(response.data.message);
                // Remove the ad from all lists where it's present
                this.all_ads = this.all_ads.filter(ad => ad.ad_id !== ad_id);
                this.name_ads = this.name_ads.filter(ad => ad.ad_id !== ad_id);
                this.camp_ads = this.camp_ads.filter(ad => ad.ad_id !== ad_id);
                this.req_ads = this.req_ads.filter(ad => ad.ad_id !== ad_id);
            } else {
                alert(`Failed to request to join: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error requesting to join ad:', error);
            if (error.response && error.response.data && error.response.data.message) {
                alert(`Error: ${error.response.data.message}`);
            } else {
                alert('An unexpected error occurred while requesting to join the ad.');
            }
        }
    }
}
};
</script>