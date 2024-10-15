<template>
    <Nav1 />
    <div class="container side1">
        <img src="../assets/displayinfluencer.jpg" alt="">
    </div>
    <div class="container side2">
        <div class="login container">
            <h3>Influencer Signup</h3>
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
                    <label for="category" class="form-label">Category</label>
                    <input type="text" class="form-control" id="category" v-model="category" />
                </div>
                <div class="mb-3">
                    <label for="niche" class="form-label">Niche</label>
                    <input type="text" class="form-control" id="niche" v-model="niche" />
                </div>
                <div class="mb-3">
                    <label for="reach" class="form-label">Reach</label>
                    <input type="number" class="form-control" id="reach" v-model="reach" />
                </div>
                <div class="d-flex justify-content-center">
                    <button type="submit" class="btn btn-light">Register as Influencer</button>
                </div>
            </form>
        </div>
    </div>
</template>


<style scoped>
.side1{
    margin-top: 22%;
    margin-left: -20%;
}
.side2{
    margin-top: 11%;
    margin-left: 10%;
}
.login{
    background-color: #ffbfc3;
    padding: 20px;
    border-radius: 20px;
    position: relative;
    height: 610px;
    width: 350px !important;
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
    name: "InfluencerSignUp",
    components: { Nav1 },
    data() {
        return {
            username: '',
            password: '',
            category: '',
            niche: '',
            reach: ''
        };
    },
    methods: {
        handleSubmit() {
            const influencerData = {
                username: this.username,
                password: this.password,
                category: this.category,
                niche: this.niche,
                reach: this.reach
            };

            axios
                .post("http://127.0.0.1:5000/api/influencer-signup", influencerData)
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