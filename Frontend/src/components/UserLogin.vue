<template>
    <Nav1/>
    <div class="container side1">
        <img src="../assets/displayuser.jpg" alt="">
    </div>
    <div class="container side2">
        <div class="login container">
            <h3>User Login</h3>
            <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" v-model="username">
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="password">
                </div>
                <div class="d-flex justify-content-center">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.side1 {
    margin-top: 10%;
    margin-left: -20%;
}
.side2 {
    margin-top: 20%;
    margin-left: 10%;
}
.login {
    background-color: #efc4eb;
    padding: 20px;
    border-radius: 20px;
    position: relative;
    height: 360px;
    width: 300px !important;
}
.login h3 {
    padding-top: 20px;
    text-align: center;
}
.login form {
    padding: 30px;
}
.side1 img {
    width: 450px;
}
</style>

<script>
import axios from 'axios';
import Nav1 from './Nav1.vue';

export default {
    name: "UserLogin",
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
        async handleSubmit() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/api/login', {
                    username: this.username,
                    password: this.password
                });

                if (response.data.status === 'success') {
                    const { role, access_token, sponsor_id, inf_id } = response.data;
                    localStorage.setItem('access_token', access_token);
                    localStorage.setItem("user_role", role);

                    if (role === 'sponsor') {
                        this.$router.push(`/sponsor-dashboard/${sponsor_id}`);
                    } else if (role === 'influencer') {
                        this.$router.push(`/influencer-dashboard/${inf_id}`);
                    } else {
                        this.$router.push('/user-login');
                    }
                } else {
                    alert('Login failed: ' + response.data.message);
                }
            } catch (error) {
                console.error('Login error:', error);

                if (error.response && error.response.data) {
                    alert('Login error: ' + error.response.data.error_message || error.response.data.message);
                } else {
                    alert('Login error: ' + error.message);
                }
            }
        }
    }
};
</script>
