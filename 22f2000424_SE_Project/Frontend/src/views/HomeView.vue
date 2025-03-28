<script setup>
import iitm_logo from '@/assets/iitm_logo.png';
import {ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const currentUsername = ref(route.params.username || '');
const courses_data = ref([]);

onMounted(async () => {
  // Get username from localStorage if not in route
  if (!currentUsername.value) {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      currentUsername.value = storedUsername;
    }
  }

  // Fetch courses data from API
  await fetchCoursesData();
});

async function fetchCoursesData() {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      await router.push('/login');
      return;
    }

    const response = await axios.get('http://localhost:5000/student_dashboard', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    courses_data.value = response.data.courses_data;
    console.log(courses_data.value)
  } catch (error) {
    console.error('Error fetching courses data:', error);
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      await router.push('/login');
    }
  }
}

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
  router.push('/login');
}
</script>

<template>
  <!-- Navbar Section -->
  <nav class="navbar">
    <div class="container">
      <div class="logo-section">
        <router-link @click.prevent="reloadPage" class="logo-link" to="/studentdashboard">
          <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
          <div class="title">
            <span class="institute-name">IIT Madras</span>
            <span class="program-name">Degree in Data Science and Applications</span>
          </div>          
        </router-link>
      </div>

      <div class="nav-links">
        <router-link :to="`/studentdashboard/${currentUsername}`" class="nav-item">Home</router-link>
        <router-link :to="`/profile/${currentUsername}`" class="nav-item">Profile</router-link>
        <a @click.prevent="logout" class="nav-item" style="cursor: pointer;">Logout</a>
      </div>
    </div>
  </nav>

  <!-- Course Cards Section -->
  <section class="py-4">
    <div class="courses-section">
      <h1 class="courses-header">My Current Courses</h1>
      <div class="courses-grid">
        <div v-for="course in courses_data" :key="course.id" class="course-card">
          <h2 class="course-header">{{ course.name }}</h2>
          <router-link :to="`/course/${course.id}`">
            <button class="go-to-course-btn">Go to Course</button>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Navbar Styling */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;  
  background: linear-gradient(to right,rgb(250, 60, 148),rgb(177, 68, 219));
  box-shadow: 0 8px 16px rgba(236, 31, 158, 0.3);
}

.container {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  width: 48px;
  height: 48px;
  margin-right: 12px;
}

.title {
  display: flex;
  flex-direction: column;
}

.institute-name,
.program-name {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
}

.institute-name{
  text-align:left;
}


.nav-links {
  display: flex;
  gap: 15px;
}

.nav-item {
  background-color: transparent;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-item:hover {
  background-color: #ffffff;
  /*color: #b51874;*/
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}



/* Course Card Styling */
.courses-section {
  padding: 24px;
  
}

.course-header {
  background: linear-gradient(135deg, #ff512f, #dd2476);
  color: #fff;
  padding: 12px;
  height:100px;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.course-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 20px;
  overflow: hidden;  
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #ffffff, #f3f4f6);
  display: flex;
  flex-direction: column;
}

h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align:center;
}

.go-to-course-btn {
  background-color: transparent; /* Match nav-item style */
  color:rgb(10, 96, 226);
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background-color 0.3s, color 0.3s;
  border: 2px solid #ffffff;
  cursor: pointer;
  justify-content: flex-end;
}

.go-to-course-btn:hover {
  background-color: #ffffff;
  color: #b51874;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

</style>