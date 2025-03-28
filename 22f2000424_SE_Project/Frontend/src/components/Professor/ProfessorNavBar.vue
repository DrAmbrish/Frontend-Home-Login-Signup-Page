<script setup>
import iitm_logo from '@/assets/iitm_logo.png'

function reloadPage() {
  window.location.reload();
}

</script>
<template>
  <nav class="navbar">
    <div class="container">
      <!-- Logo Section -->
      <div class="logo-section" @click="reloadPage" style="cursor:pointer">
        <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
          <div class="institute-name">
            <span >IIT Madras </span>
          </div>
          <div class="course-info">
            <span class="course-term">Jan 2025 - </span> 
            <span class="course-term">Professor Dashboard</span>           
          </div> 
       
      </div>

      <!-- Navigation Links -->
      <div class="nav-links">
        <router-link to="/professorpage" class="nav-item">Home</router-link>
        <router-link to="/professorchatbot" class="nav-item">ChatBot</router-link>
        <router-link to="/professor/profile" class="nav-item">Profile</router-link>
        <router-link to="/" class="nav-item">Logout</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Navbar styling */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 8px 16px rgba(236, 31, 158, 0.2);
}

.container {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}


/* Logo section styling */
.logo-section {
  display: flex;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 12px;
}
.institute-name{
  font-size: 18px;
  font-weight: bold;
  color:rgb(68, 33, 33);
  gap: 20px;
}

.course-info {
  display: flex;
  align-items: center;  
  background: linear-gradient(to right,rgb(250, 60, 148),rgb(177, 68, 219));
  box-shadow: 0 5px 5px rgba(245, 103, 238, 0.68);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px; 
  margin-left: 12px; 
}

.course-term {
  color:rgb(248, 242, 242);  
  font-weight: bold;
  margin-right: 6px;
}

.course-title {
  color:rgb(248, 242, 242);  
  font-weight: bold;
}



/* Navigation links styling */
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-item {
  background-color: transparent;
  /*color:rgba(136, 4, 54, 0.52);*/
  color:rgb(68, 33, 33);
  text-decoration: none;
  
  font-size: 18px;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-item:hover {
  background: linear-gradient(to right,rgb(250, 60, 148),rgb(177, 68, 219));
  box-shadow: 0 5px 5px rgba(245, 103, 238, 0.68);
  color:  #ffffff;
}
</style>