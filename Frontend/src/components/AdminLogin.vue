<template>
    <Nav1/>
    <div class="container side1">
        <img src="../assets/displayadmin.jpg" alt="">
    </div>
    <div class="container side2">
        <div class="login container">
            <h3>Admin Login</h3>
            <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" aria-describedby="emailHelp" v-model="username" >
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password"  v-model="password">
                </div>
                <div class="d-flex justify-content-center">
                    <button type="submit" class="btn btn-primary">Submit</button>
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
    margin-top: 20%;
    margin-left: 10%;
}
.login{
    background-color: #dff2fd;
    padding: 20px;
    border-radius: 20px;
    position: relative;
    height: 360px;
    width: 300px !important;
}
.login h3{
    padding-top: 20px;
    text-align: center;
}
.login form{
    padding: 30px;
}
.side1 img{
    width: 450px;
}
</style>

<script>
import axios from 'axios';
import Nav1 from './Nav1.vue';

export default {
    name: "AdminLogin",
    components: {
        Nav1
    },
    data() {
        return {
            username: '',
            password: ''
        };
    },
    methods: {
        handleSubmit() {
            if (!this.username || !this.password) {
                alert("Please Enter Both fields!");
                return;
            }
            
            const userData = {
                username: this.username,
                password: this.password
            };

            axios
                .post("http://127.0.0.1:5000/api/admin-login", userData)
                .then((response) => {
                    if (response.data.status === "success") {
                        localStorage.setItem("access_token", response.data.access_token);
                        localStorage.setItem("user_role", 'admin'); // Set user role
                        // alert("Successfully Logged in!");
                        this.$router.push({ name: 'AdminDashboard' });
                    } else {
                        alert("Invalid credentials!");
                    }
                })
                .catch((error) => {
                    console.error(error);
                    if (error.response && error.response.data) {
                        alert(error.response.data.error_message);
                    } else {
                        alert("An error occurred while logging in!");
                    }
                });
        }
    }
};
</script>
