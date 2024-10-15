<template>
    <div class="container p1">
        <h2>Welcome back Admin!</h2>

        <!-- Display sponsors with pending signup request -->
        <div class="row">
            <div class="col-7">
                <div class="content" v-if="sponsors.length">
            <h4>Pending Sponsor SignUp Requests:</h4>
            <div class="vstack gap-3" v-for="sponsor in sponsors" :key="sponsor.sponsor_id">
                <div class="hstack hs1 gap-3">
                    <div class="p-2"><strong>Sponsor ID: </strong>{{ sponsor.sponsor_id }}</div>
                    <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ sponsor.org_name }}</div>
                    <div class="p-2 ms-auto">
                        <button class="btn btn-success" @click="approveSponsor(sponsor.sponsor_id)">Approve</button>
                    </div>
                    <div class="p-2 ms-auto">
                        <button class="btn btn-danger" @click="declineSponsor(sponsor.sponsor_id)">Decline</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="content" v-else>
            <h4>Pending Sponsor SignUp Requests:</h4>
            <div class="hstack hs2 gap-3">
                <div class="p-2 ms-auto"></div>
                <p class="p-2">No Pending SignUp Requests of Sponsors!</p>
                <div class="p-2 ms-auto"></div>
            </div>
        </div>



        <!-- Display declined sponsors -->
        <div class="content" v-if="decsponsors.length">
            <h4>Declined Sponsor Signup Requests:</h4>
            <div class="vstack gap-3" v-for="sponsor in decsponsors" :key="sponsor.sponsor_id">
                <div class="hstack hs3 gap-3">
                    <div class="p-2"><strong>Sponsor ID: </strong>{{ sponsor.sponsor_id }}</div>
                    <div class="p-2 ms-auto"><strong>Organization Name: </strong>{{ sponsor.org_name }}</div>
                    <div class="p-2 ms-auto">
                        <button class="btn btn-warning" @click="validateSponsor(sponsor.sponsor_id)">Validate</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="content" v-else>
            <h4>Declined Sponsor Signup Requests:</h4>
            <div class="hstack hs2 gap-3">
                <div class="p-2 ms-auto"></div>
                <p class="p-2">No Declined Sponsors yet!</p>
                <div class="p-2 ms-auto"></div>
            </div>
        </div>
            </div>
            <div class="col-5">
                <!-- Inside the <div class="col-6">, add this -->
                <div class="content" v-if="influencers.length">
                    <h4>Influencers List:</h4>
                    <div class="vstack gap-3" v-for="influencer in influencers" :key="influencer.inf_id">
                        <div class="hstack gap-3 hs4">
                            <div class="p-2"><strong>Influencer ID: </strong>{{ influencer.inf_id }}</div>
                            <div class="p-2 ms-auto"><strong>Username: </strong>{{ influencer.username }}</div>
                            <div class="p-2 ms-auto"><strong>Category: </strong>{{ influencer.category }}</div>
                            <div class="p-2 ms-auto"><strong>Niche: </strong>{{ influencer.niche }}</div>
                            <!-- <div class="p-2 ms-auto"><strong>Reach: </strong>{{ influencer.reach }}</div> -->
                            <div class="p-2 ms-auto" v-if="isnotFlagged(influencer)"><button class="btn btn-danger" @click="flagInfluencer(influencer.inf_id)">Flag</button></div>
                            <div class="p-2 ms-auto" v-if="isFlagged(influencer)"><button class="btn btn-warning" @click="unflagInfluencer(influencer.inf_id)">UnFlag</button></div>
                            <!-- <div class="p-2 ms-auto"><strong>Flag: </strong>{{ influencer.flag }}</div> -->
                        </div>
                    </div>
                </div>
                <div class="content" v-else>
                    <h4>Influencers List:</h4>
                    <div class="hstack hs2 gap-3">
                        <p class="p-2">No Influencers Found!</p>
                    </div>
                </div>

            </div>
        </div>

        
    </div>
    <AdminNav />
</template>

<style>
.content {
    margin-top: 25px;
}
.vstack {
    margin-top: 25px;
}
.p1 {
    position: absolute;
    left: 5%;
    top: 12%;
}
.hs1{
    border-radius: 10px;
    padding: 10px;
    width: 680px;
    background-color: rgb(255, 251, 141);
}
.hs2 {
    border-radius: 10px;
    padding: 10px;
    width: 680px;
    margin-top: 45px;
    color: rgb(83, 0, 0);
    background-color: rgb(255, 219, 225);
}
.hs4{
    border-radius: 10px;
    padding: 10px;
    background-color: rgb(202, 242, 255);
    width: 600px;
}
.hs3 {
    border-radius: 10px;
    padding: 10px;
    width: 680px;
    background-color: rgb(255, 219, 225);
}
</style>

<script>
import axios from 'axios';
import AdminNav from './AdminNav.vue';

export default {
    name: "AdminDashboard",
    components: {
        AdminNav
    },
    data() {
        return {
            sponsors: [],
            decsponsors: [],
            influencers: []
        };
    },
    created(){
        this.fetchInfluencers();
        this.pendingSponsors();
        this.declinedSponsors();
    },
    methods: {
        isFlagged(inf){
            return inf.flag === 'flag';
        },
        isnotFlagged(inf){
            return inf.flag === 'unflag';
        },
        async flagInfluencer(inf_id) {
            try {
                const response = await axios.put(`http://127.0.0.1:5000/api/flag-influencer/${inf_id}`, null, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    alert(response.data.message);
                    this.fetchInfluencers(); // Refresh the list
                } else {
                    console.error('Error flagging influencer:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async unflagInfluencer(inf_id) {
            try {
                const response = await axios.put(`http://127.0.0.1:5000/api/unflag-influencer/${inf_id}`, null, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    alert(response.data.message);
                    this.fetchInfluencers(); // Refresh the list
                } else {
                    console.error('Error unflagging influencer:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async fetchInfluencers() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/all-influencers', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    this.influencers = response.data.influencerdata;
                } else {
                    console.error('Error loading influencers:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async pendingSponsors() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/pending-sponsor-signup', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    this.sponsors = response.data.sponsordata;
                } else {
                    console.error('Error loading sponsors:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async declinedSponsors(){
            try{
                const response = await axios.get('http://127.0.0.1:5000/api/declined-sponsors-list', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });
                
                if (response.data.status === 'success') {
                    this.decsponsors = response.data.dec_sponsors;
                } else {
                    console.error('Error loading declined sponsors:', response.data.message);
                }
            } catch (error) {
                console.error('API Error: ', error);
            }
        },
        async validateSponsor(sponsor_id){
            try {
                const response = await axios.put(`http://127.0.0.1:5000/api/validate-sponsor/${sponsor_id}`, null, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    alert(response.data.message);

                    // Remove the sponsor from declined sponsors list
                    this.decsponsors = this.decsponsors.filter(sponsor => sponsor.sponsor_id !== sponsor_id);

                    // Refresh the pending sponsors list to include the validated sponsor
                    this.pendingSponsors();
                } else {
                    console.error('Error validating sponsor:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async approveSponsor(sponsor_id) {
            try {
                const response = await axios.put(`http://127.0.0.1:5000/api/approve-sponsor/${sponsor_id}`, null, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    alert(response.data.message);

                    // Update the pending sponsors list after approval
                    this.sponsors = this.sponsors.filter(sponsor => sponsor.sponsor_id !== sponsor_id);
                } else {
                    console.error('Error approving sponsor:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
        async declineSponsor(sponsor_id) {
            try {
                const response = await axios.put(`http://127.0.0.1:5000/api/decline-sponsor/${sponsor_id}`, null, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    alert(response.data.message);

                    // Update the pending sponsors list after decline
                    this.sponsors = this.sponsors.filter(sponsor => sponsor.sponsor_id !== sponsor_id);

                    // Refresh the declined sponsors list
                    this.declinedSponsors();
                } else {
                    console.error('Error declining sponsor:', response.data.message);
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        },
    }
};
</script>
