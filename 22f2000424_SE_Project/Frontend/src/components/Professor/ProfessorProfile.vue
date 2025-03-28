<template>
  <ProfessorNavBar/>
  <div class="profile-page">
    <div class="profile-container">
      <div class="profile-header">
        <!-- Profile image on top -->
        <div class="image-container">
          <img
              :src="studentProfile"
              alt="Profile Picture"
              class="profile-image"
          />
        </div>
        <!-- Student details below the image -->
        <div class="student-details">
          <h2 class="student-name">{{ student.name }}</h2>
          <p class="degree-level">Degree: {{ student.degree }}</p>
          <p class="branch">Branch: {{ student.branch }}</p>
          <p class="college-name">College: {{ student.college }}</p>
        </div>
      </div>

      <!-- Courses section -->
      <div class="courses-section">
        <h3>Selected Courses</h3>
        <ul>
          <li v-for="(course, index) in student.courses" :key="index">{{ course }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminNavBar from "@/components/Admin/AdminNavBar.vue";
import studentProfile from "@/assets/studentProfile.png";
import ProfessorNavBar from "@/components/Professor/ProfessorNavBar.vue";

// Sample student data (can later be fetched from the backend)
const student = {
  name: "Atharva Sarbhukan",
  degree: "B.S. Degree in Data Science and Applications",
  branch: "Data Science and Programming",
  college: "Indian Institute of Technology, Madras",
  courses: [
    "Modern Application Development - 1",
    "Modern Application Development - 2",
    "Machine Learning Practice",
    "Business Data Management"
  ]
};
</script>


<style scoped>

.profile-page {
  font-family: 'Inter', Arial, sans-serif;
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  padding: 50px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-container {
  width: 100%;
  max-width: 900px;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 20px;
  /*box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);*/
  box-shadow: 0 10px 16px rgba(245, 103, 238, 0.68);
  
  transition: box-shadow 0.3s ease;
}

.profile-container:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
}

.image-container {
  padding-bottom: 25px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 100%;
  height: 320px;
  border-radius: 12px; /* Square with rounded corners */
  object-fit: cover;
  border: 2px solid #e0e0e0;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  transition: transform 0.2s ease-in-out;
}

.profile-image:hover {
  transform: scale(1.05); /* Slight zoom on hover */
}


.student-details {
  text-align: left;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  border: 1px solid #e0e0e0;
}

.student-details h2 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  border-bottom: 2px solid #007bff;
  display: inline-block;
  padding-bottom: 4px;
}

.student-details p {
  font-size: 16px;
  color: #555;
  margin: 8px 0;
  line-height: 1.6;
  display: flex;
  align-items: center;
}

.student-details strong {
  font-weight: 500;
  color: #007bff;
  width: 150px; /* Aligns all labels vertically */
  display: inline-block;
}

.student-details span {
  flex-grow: 1;
}


.courses-section {
  margin-top: 30px;
}

.courses-section h3 {
  font-size: 24px;
  font-weight: 600;
  color: #007bff;
  margin-bottom: 16px;
  text-align: left;
}

.courses-section ul {
  list-style: none;
  padding: 0;
}

.courses-section li {
  background-color: #f8f9fa;
  padding: 12px 20px;
  margin-bottom: 10px;
  border-radius: 8px;
  font-size: 16px;
  color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.courses-section li:hover {
  background-color: #e9ecef;
}

.course-description {
  font-size: 14px;
  color: #777;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .student-details {
    text-align: center;
  }
}

</style>
