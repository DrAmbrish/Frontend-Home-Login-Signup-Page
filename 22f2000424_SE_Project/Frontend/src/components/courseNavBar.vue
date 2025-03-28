<script setup>
import iitm_logo from '@/assets/iitm_logo.png'
import {useRouter} from 'vue-router'; // Import the useRouter composable
import {useRoute} from 'vue-router'; // Import useRoute if needed for getting current username
import {ref, onMounted} from 'vue';

// Get router instance
const router = useRouter();
const route = useRoute();
const currentUsername = ref('');

// Get username on component mount
onMounted(() => {
  const storedUsername = localStorage.getItem('username') || sessionStorage.getItem('username');
  if (storedUsername) {
    currentUsername.value = storedUsername;
    console.log("Current username:", currentUsername.value);
  } else {
    console.log("No username found in storage");
  }
});

function reloadPage() {
  window.location.reload();
}

function logout() {
  // Clear tokens from both localStorage and sessionStorage for consistency
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('username');

  sessionStorage.removeItem('access_token');
  sessionStorage.removeItem('refresh_token');
  sessionStorage.removeItem('username');

  console.log('Logged out, credentials cleared');

  // Redirect to login page
  router.push('/login');
}
</script>

<template>
  <nav class="navbar">
    <div class="container">
      <!-- Logo Section -->
      <div class="logo-section">
        <!-- Use router-link instead of <a> -->
        <router-link @click.prevent="reloadPage" to="/studentdashboard" class="logo-link">
          <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
          <div class="institute-name">
            <span >IIT Madras </span>
          </div>
          <div class="course-info">
            <span class="course-term">Jan 2025</span>
            
          </div>          
        </router-link>
      </div>

      <!-- Navigation Links -->
      <div class="nav-links">
        <router-link :to="`/studentdashboard/${currentUsername}`" class="nav-item">Home</router-link>
<!--        <router-link to="/studentchatbot" class="nav-item">ChatBot</router-link>-->
        <router-link :to="`/profile/${currentUsername}`" class="nav-item">Profile</router-link>
        <a @click.prevent="logout" class="nav-item" style="cursor: pointer;">Logout</a>
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
  /*background-color: #ffffff;*/
  background: linear-gradient(to right,rgb(250, 60, 148),rgb(177, 68, 219));
  box-shadow: 0 5px 5px rgba(245, 103, 238, 0.68);
  /*color:rgb(248, 242, 242);*/ 
  color:  #ffffff;
}

</style>