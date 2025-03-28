<script setup>
import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
import studentProfile from "@/assets/studentProfile.png";
import {ref, onMounted} from 'vue';
import axios from 'axios';


const instructor = ref({
 id: null,
 name: '',
 username: '',
 email: '',
 role: '',
 created_at: '',
 last_login: ''
});


const isLoading = ref(true);
const error = ref(null);


// Fetch Instructor profile data from API
const fetchInstructorProfile = async () => {
 try {
   isLoading.value = true;
   error.value = null;


   const token = localStorage.getItem("access_token");
   if (!token) {
     error.value = "No access token found. Please log in again.";
     isLoading.value = false;
     console.error("No access token found");
     return;
   }


   const response = await axios.get("http://localhost:5000/instructor_details", {
     headers: {
       Authorization: `Bearer ${token}`
     }
   });


   console.log("API Response:", response.data);


   // Update the instructor data with API response
   const profileData = response.data;
   instructor.value = {
     ...instructor.value,
     name: profileData.name,
     email: profileData.email,
     username: profileData.username,
     role: profileData.role,
     created_at: profileData.created_at,
     last_login: profileData.last_login
   };


   isLoading.value = false;
 } catch (err) {
   error.value = err.response?.data?.message || 'Failed to load instructor details';
   isLoading.value = false;
   console.error("Error fetching instructor profile:", err);
 }
};


// Format date function
const formatDate = (dateString) => {
 if (!dateString) return 'N/A';
 return new Date(dateString).toLocaleDateString('en-US', {
   year: 'numeric',
   month: 'long',
   day: 'numeric'
 });
};


// Call the fetch function when component mounts
onMounted(() => {
 fetchInstructorProfile();
});
</script>


<template>
 <InstructorNavBar/>
 <div class="profile-page">
   <div class="profile-container">
     <div class="profile-header">
       <h1>Instructor Profile</h1>


       <!-- Loading state -->
       <div v-if="isLoading" class="loading-state">
         Loading instructor details...
       </div>


       <!-- Error state -->
       <div v-else-if="error" class="error-message">
         {{ error }}
       </div>


       <!-- Content when data is loaded -->
       <div v-else>
         <!-- Profile image on top -->
         <div class="image-container">
           <img
               :src="studentProfile"
               alt="Profile Picture"
               class="profile-image"
           />
         </div>


         <!-- Instructor details below the image -->
         <div class="instructor-details">
           <h2 class="instructor-name">{{ instructor.name }}</h2>
           <p class="instructor-role">Role: {{ instructor.role }}</p>
           <p class="instructor-email">Email: {{ instructor.email }}</p>
           <p class="instructor-username">Username: {{ instructor.username }}</p>
         </div>
       </div>
     </div>


     <!-- Additional information section -->
     <div v-if="!isLoading && !error" class="additional-info">
       <h3>Account Information</h3>
       <div class="info-item">
         <span class="info-label">Account Created:</span>
         <span class="info-value">{{ formatDate(instructor.created_at) }}</span>
       </div>
       <div class="info-item">
         <span class="info-label">Last Login:</span>
         <span class="info-value">{{ formatDate(instructor.last_login) }}</span>
       </div>
     </div>
   </div>
 </div>
</template>


<style scoped>
.profile-page {
 font-family: Arial, sans-serif;
 padding: 50px;
}


.profile-container {
 max-width: 800px;
 margin: 0 auto;
 padding: 20px;
 background-color: #f9f9f9;
 border-radius: 8px;
 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}


.profile-header {
 display: flex;
 flex-direction: column;
 align-items: center;
 margin-bottom: 30px;
}


.image-container {
 padding-bottom: 25px;
 display: flex;
 justify-content: center;
 margin-bottom: 20px;
}


.profile-image {
 width: 150px;
 height: 150px;
 border-radius: 50%;
 object-fit: cover;
}


.instructor-details {
 text-align: center;
}


.instructor-details h2 {
 margin: 0;
 font-size: 24px;
 font-weight: bold;
}


.instructor-details p {
 margin: 5px 0;
 font-size: 16px;
}


.additional-info {
 margin-top: 30px;
 padding: 20px;
 background-color: #f0f0f0;
 border-radius: 8px;
}


.additional-info h3 {
 font-size: 22px;
 font-weight: bold;
 text-align: center;
 margin-bottom: 15px;
}


.info-item {
 display: flex;
 justify-content: space-between;
 padding: 8px 0;
 border-bottom: 1px solid #ddd;
}


.info-item:last-child {
 border-bottom: none;
}


.info-label {
 font-weight: bold;
}


.loading-state {
 text-align: center;
 padding: 20px;
 font-style: italic;
 color: #666;
}


.error-message {
 text-align: center;
 padding: 20px;
 color: #d32f2f;
 font-weight: bold;
}
</style>

