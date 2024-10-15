<!-- AdminStats.vue -->
<template>
    <div class="out">
        <div class="row">
            <div class="col">
                <div class="container">
                    <h4 align="center">Ad Status Distribution</h4>
                    <div v-if="loading" class="text-center">
                        <p>Loading...</p>
                    </div>
                    <div v-else>
                        <img :src="pieChartSrc" alt="Ad Status Pie Chart" class="img-fluid" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <AdminNav />
  </template>
  
  <script>
  import axios from 'axios';
  import AdminNav from './AdminNav.vue';
  
  export default {
    name: "AdminStats",
    components: {
      AdminNav
    },
    data() {
      return {
        pieChartSrc: '',
        loading: true
      };
    },
    async created() {
      await this.fetchPieChart();
    },
    methods: {
      async fetchPieChart() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/ad-status-piechart', {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          });
  
          if (response.data.status === 'success') {
            this.pieChartSrc = `data:image/png;base64,${response.data.data}`;
          } else {
            console.error('Error fetching pie chart:', response.data.message);
            alert(`Error: ${response.data.message}`);
          }
        } catch (error) {
          console.error('API Error:', error);
          alert('An error occurred while fetching the pie chart.');
        } finally {
          this.loading = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .out{
    position: absolute;
    left: 30%;
    top: 12%;
  }
  img {
    width: 560px;
  }
  </style>
  