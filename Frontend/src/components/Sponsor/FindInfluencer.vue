<!-- FindInfluencer.vue -->
<template>
  <div class="container ch">
    <div class="row">
      <div class="col-2"></div>
      <div class="col-3">
        <h4 align="center">Find Influencer</h4>
      </div>
      <div class="col-5">
        <form class="d-flex" @submit.prevent="searchInfluencers">
          <input v-model="searchQuery" class="form-control me-2" type="search" placeholder="Search by name, category, or niche" aria-label="Search">
          &nbsp;&nbsp;&nbsp;
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </div>
    <hr>

    <div class="row mt-4" v-if="unameinfluencers.length">
      <h5>Found by Username:</h5>
      <table class="table table-warning table-striped">
        <thead>
          <tr align="center">
            <th><strong>Username</strong></th>
            <th><strong>Category</strong></th>
            <th><strong>Niche</strong></th>
            <th><strong>Reach</strong></th>
            <th><strong>Request for Ad</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inf in unameinfluencers" :key="inf.inf_id" align="center">
            <td>{{ inf.username }}</td>
            <td>{{ inf.category }}</td>
            <td>{{ inf.niche }}</td>
            <td>{{ inf.reach }}</td>
            <td><router-link :to="`/find-influencer/${sponsorId}/ad-request/${inf.inf_id}`" class="btn btn-dark">Request for Ad</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>


    <div class="row mt-4" v-if="catinfluencers.length">
      <h5>Found by Category:</h5>
      <table class="table table-success table-striped">
        <thead>
          <tr align="center">
            <th><strong>Username</strong></th>
            <th><strong>Category</strong></th>
            <th><strong>Niche</strong></th>
            <th><strong>Reach</strong></th>
            <th><strong>Request for Ad</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inf in catinfluencers" :key="inf.inf_id" align="center">
            <td>{{ inf.username }}</td>
            <td>{{ inf.category }}</td>
            <td>{{ inf.niche }}</td>
            <td>{{ inf.reach }}</td>
            <td><router-link :to="`/find-influencer/${sponsorId}/ad-request/${inf.inf_id}`" class="btn btn-dark">Request for Ad</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>


    <div class="row mt-4" v-if="nicheinfluencers.length">
      <h5>Found by Niche:</h5>
      <table class="table table-primary table-striped">
        <thead>
          <tr align="center">
            <th><strong>Username</strong></th>
            <th><strong>Category</strong></th>
            <th><strong>Niche</strong></th>
            <th><strong>Reach</strong></th>
            <th><strong>Request for Ad</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inf in nicheinfluencers" :key="inf.inf_id" align="center">
            <td>{{ inf.username }}</td>
            <td>{{ inf.category }}</td>
            <td>{{ inf.niche }}</td>
            <td>{{ inf.reach }}</td>
            <td><router-link :to="`/find-influencer/${sponsorId}/ad-request/${inf.inf_id}`" class="btn btn-dark">Request for Ad</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>


    <div class="row mt-4" v-if="!searched && !unameinfluencers.length && !catinfluencers.length && !nicheinfluencers.length">
      <h5>All Influencers:</h5>
      <table class="table table-striped">
        <thead>
          <tr align="center">
            <th><strong>Username</strong></th>
            <th><strong>Category</strong></th>
            <th><strong>Niche</strong></th>
            <th><strong>Reach</strong></th>
            <th><strong>Request for Ad</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inf in allinfluencers" :key="inf.inf_id" align="center">
            <td>{{ inf.username }}</td>
            <td>{{ inf.category }}</td>
            <td>{{ inf.niche }}</td>
            <td>{{ inf.reach }}</td>
            <td><router-link :to="`/find-influencer/${sponsorId}/ad-request/${inf.inf_id}`" class="btn btn-dark">Request for Ad</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="searched && !unameinfluencers.length && !catinfluencers.length && !nicheinfluencers.length">
      <p align="center" style="color: red;">No influencers found for "{{ searchQuery }}"</p>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <SponsorNav />
  </div>
</template>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
  name: 'FindInfluencer',
  components: {
    SponsorNav
  },
  data() {
    return {
      allinfluencers: [],
      unameinfluencers: [],
      catinfluencers: [],
      nicheinfluencers: [],
      searchQuery: '', // Add searchQuery to data
      searched: false,
      error: '',
      sponsorId: localStorage.getItem('sponsor_id'),
    };
  },
  created(){
    this.fetchallInfluencers();
  },
  methods: {
  async searchInfluencers() {
    if (this.searchQuery.trim() === '') {
      // If the search query is empty, show all influencers
      this.fetchallInfluencers();
    } else {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/influencer-search', {
          params: { query: this.searchQuery },  // Ensure query is passed
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
           }
        });
        this.allinfluencers = response.data.inf_all;
        this.unameinfluencers = response.data.inf_uname;
        this.catinfluencers = response.data.inf_cat;
        this.nicheinfluencers = response.data.inf_niche;
        this.searched = true;
      } catch (error) {
        console.error('Error fetching influencers:', error);
        this.error = 'Error fetching influencers: ' + error;
      }
    }
  },

  async fetchallInfluencers() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/influencer-search', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
         }
      });
      this.allinfluencers = response.data.inf_all;
      this.unameinfluencers = [];
      this.catinfluencers = [];
      this.nicheinfluencers = [];
      this.searched = false;
    } catch (error) {
      console.error('Error fetching all influencers:', error);
      this.error = 'Error fetching all influencers: ' + error;
    }
  }
}
};
</script>

<style>
.ch {
  position: absolute;
  left: 7%;
  top: 15%;
  width: 90%;
}
</style>