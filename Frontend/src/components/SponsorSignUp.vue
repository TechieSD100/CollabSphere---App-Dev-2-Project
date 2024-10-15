<template>
    <Nav1 />
    <div class="container side1">
        <img src="../assets/displaysponsor.jpg" alt="">
    </div>
    <div class="container side2">
        <div class="login container">
            <h3>Sponsor Signup</h3>
            <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" v-model="username" />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="password" />
                </div>
                <div class="mb-3">
                    <label for="organisation" class="form-label">Organisation</label>
                    <input type="text" class="form-control" id="organisation" v-model="organisation" />
                </div>
                <div class="d-flex justify-content-center">
                    <button type="submit" class="btn btn-primary">Register as Sponsor</button>
                </div>
            </form>
        </div>
    </div>
</template>


<style scoped>
.side1{
    margin-top: 10%;
    margin-left: -20%;
}
.side2{
    margin-top: 10%;
    margin-left: 10%;
}
.login{
    background-color: #a5ccff;
    padding: 20px;
    border-radius: 20px;
    position: relative;
    height: 450px;
    width: 300px !important;
}
.login h3{
    padding-top: 20px;
    text-align: center;
}
.login form{
    padding: 30px;
    padding-top: 15px;
}
.login form button{
    margin-top: 15px;
}
.side1 img{
    width: 450px;
}
</style>


<script>
import axios from 'axios';
import Nav1 from './Nav1.vue';

export default {
    name: "SponsorSignUp",
    components: { Nav1 },
    data() {
        return {
            username: '',
            password: '',
            organisation: ''
        };
    },
    methods: {
        handleSubmit() {
            const sponsorData = {
                username: this.username,
                password: this.password,
                org_name: this.organisation
            };

            axios
                .post("http://127.0.0.1:5000/api/sponsor-signup", sponsorData)
                .then((response) => {
                    if (response.data.status === "success") {
                        alert("Signup Successful!");
                        this.$router.push("/user-login");
                    } else {
                        alert(response.data.message);
                    }
                })
                .catch((error) => {
                    console.error(error);
                    alert("An error occurred during the signup process.");
                });
        }
    }
};
</script>
