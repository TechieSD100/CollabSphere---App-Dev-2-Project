<template>
    <nav class="navbar navbar-expand-lg bg-warning">
        <div class="container-fluid">
            <strong><a class="navbar-brand" href="#">Sponsor Dashboard</a></strong>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <!-- Dynamically include the influencer ID in the URL -->
                    <li class="nav-item">
                        <router-link :to="`/sponsor-dashboard/${sponsorId}`" class="btn btn-light">Profile</router-link>
                    </li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item">
                        <router-link :to="`/sponsor-campaigns/${sponsorId}`" class="but btn btn-info">My Campaigns</router-link>
                    </li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item">
                        <router-link :to="`/find-influencer/${sponsorId}`" class="btn btn-light">Find Influencers</router-link>
                    </li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item">
                        <router-link :to="`/sponsor-stats/${sponsorId}`" class="but btn btn-primary">Stats</router-link>
                    </li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item">
                        <a class="btn btn-danger" @click="logout">Logout</a>
                    </li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
  name: "SponsorNav",
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id') , // Fetch the influencer ID from localStorage
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/user-login');
      window.alert('You are logged out.');
    }
  }
};
</script>

<style>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 10px;
}
</style>
