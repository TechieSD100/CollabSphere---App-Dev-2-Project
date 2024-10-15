<template>
    <nav class="navbar navbar-expand-lg nv1">
        <div class="container-fluid">
            <strong><a class="navbar-brand" href="#">Influencer Engagement & Sponsorship Coordination Platform</a></strong>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/user-login" class="btn btn-light">User Login</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/admin-login" class="but btn btn-info">Admin Login</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/influencer-signup" class="btn btn-light">Influencer Sign Up</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/sponsor-signup" class="btn btn-primary">Sponsor Sign Up</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    
                </ul>
            </div>
        </div>
    </nav>
</template>

<style>
.navbar{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 10px;
}
.nv1{
    background-color: rgb(255, 205, 235);
}
</style>


<script>
export default
{
    name : "Nav1",
};
</script>