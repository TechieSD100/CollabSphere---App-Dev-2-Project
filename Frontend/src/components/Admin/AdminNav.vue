<template>
    <nav class="navbar navbar-expand-lg nv">
        <div class="container-fluid">
            <strong><a class="navbar-brand" href="#">Admin Dashboard</a></strong>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/admin-dashboard" class="btn btn-success">Dashboard</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/admin-stats" class="but btn btn-light">Stats</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <li class="nav-item"><router-link to="/admin-login" class="btn btn-danger">Logout</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li>
                    <!-- <li class="nav-item"><router-link to="/sponsor-signup" class="btn btn-primary">Sponsor Sign Up</router-link></li>
                    <li class="nav-item"><a href="" class="nav-link"></a></li> -->
                    
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
.nv{
    background-color: #d4ffb5;
}
</style>


<script>
export default
{
    name : "AdminNav",
};
</script>