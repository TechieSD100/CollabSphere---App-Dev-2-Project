<template>
    <div class="container p1">
        <div class="content">
            <h4>Most Common Campaigns:</h4>
            <div v-if="chartImage">
                <img :src="'data:image/png;base64,' + chartImage" alt="Popular Campaigns Pie Chart" />
            </div>
            <div v-else>
                <p>Loading chart...</p>
            </div>
        </div>
    </div>
    <InfluencerNav />
</template>

<script>
import axios from 'axios';
import InfluencerNav from './InfluencerNav.vue';

export default {
  name: 'InfluencerStats',
  components: {
    InfluencerNav
  },
  data() {
    return {
      chartImage: null
    };
  },
  created() {
    this.fetchPopularCampaigns();
  },
  methods: {
    async fetchPopularCampaigns() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/popular-campaigns', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.data.status === 'success') {
          this.chartImage = response.data.image;
        } else {
          console.error('Error fetching popular campaigns:', response.data.message);
        }
      } catch (error) {
        console.error('API Error:', error);
      }
    }
  }
};
</script>

<style>
.content {
    text-align: center;
}
img {
    width: 570px;
}
.p1{
    top: 10%;
}
</style>
