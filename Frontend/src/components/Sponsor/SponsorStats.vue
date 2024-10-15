<template>
    <div class=".out">
        <div class="container cont">
            <h4 align="center">Most Expensive Ads</h4>
            <div v-if="loading" class="text-center">
                <p>Loading...</p>
            </div>
            <div v-else>
                <img :src="barChartSrc" alt="Most Expensive Ads Bar Chart" />
            </div>
        </div>
    </div>
    <SponsorNav />
</template>

<script>
import axios from 'axios';
import SponsorNav from './SponsorNav.vue';

export default {
    name: "MostExpensiveAds",
    components: {
        SponsorNav
    },
    data() {
        return {
            barChartSrc: '',
            loading: true,
        };
    },
    async created() {
        await this.fetchBarChart();
    },
    methods: {
        async fetchBarChart() {
            const sponsorId = this.$route.params.sponsor_id;
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/most-expensive-ads/${sponsorId}`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });

                if (response.data.status === 'success') {
                    this.barChartSrc = `data:image/png;base64,${response.data.data}`;
                } else {
                    console.error('Error fetching bar chart:', response.data.message);
                    alert(`Error: ${response.data.message}`);
                }
            } catch (error) {
                console.error('API Error:', error);
                alert('An error occurred while fetching the bar chart.');
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
}
.cont{
    margin-left: 24%;
}
img {
    width: 800px;
}
</style>
