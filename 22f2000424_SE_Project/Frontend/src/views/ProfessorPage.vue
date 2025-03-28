<template>
  <ProfessorNavBar/>
  <div class="container">
    <div class="sidebar">
      <button @click="setActiveComponent('ProfessorDetails')">Professor Details</button>
      <button @click="setActiveComponent('CourseDetails')">Course Details</button>
      <button @click="setActiveComponent('TopQueries')">Top Queries</button>
      <button @click="setActiveComponent('PendingInstructors')">Pending Instructors</button>
      <button @click="setActiveComponent('AddLesson')">Add Lesson</button>
    </div>
    
    <div class="content">
      <div v-if="activeComponent === 'ProfessorDetails'">
        <h2>Professor Details</h2>
        <ul v-if="professordetails">
          <li><strong>Name:</strong> {{ professordetails.name }}</li>
          <li><strong>Email:</strong> {{ professordetails.email }}</li>
          <li><strong>Role:</strong> {{ professordetails.role }}</li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

      <div v-if="activeComponent === 'TopQueries'">
        <h2>Top Support Queries</h2>
        <ul v-if="queries.length">
          <li v-for="query in queries" :key="query.query">
            {{ query.query_text }} - {{ query.count }} times
          </li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

       <!-- Course Details -->
    <div v-if="activeComponent === 'CourseDetails'">
      <h2>Course Details</h2>
      <ul v-if="coursedetails.length">
        <li v-for="course in coursedetails" :key="course.id">
          <strong>Course Name:</strong> {{ course.name }} <br />
          <strong>Description:</strong> {{ course.description }} <br />
          <strong>Total Assignments:</strong> {{ course.total_assignments }} <br />
          <strong>Created At:</strong> {{ course.created_at }}
        </li>
      </ul>
      <p v-else>No course details found.</p>
    </div>

     <!-- Pending Instructors -->
     <div v-if="activeComponent === 'PendingInstructors'">
        <h2>Pending Instructor Requests</h2>
        <ul v-if="pendingInstructors.length">
          <li v-for="request in pendingInstructors" :key="request.id">
            <strong>ID:</strong> {{ request.id }} <br />
            <strong>Instructor ID:</strong> {{ request.instructor_id }} <br />
            <strong>Status:</strong> {{ request.status }} <br />
            <strong>Created At:</strong> {{ request.created_at }} <br />
            <button @click="approveInstructor(request.id, 'Approved')">Approve</button>
            <button @click="approveInstructor(request.id, 'Rejected')">Reject</button>
          </li>
        </ul>
        <p v-else>No pending instructor requests.</p>
      </div>

      <!-- Add Lesson -->
      <div v-if="activeComponent === 'AddLesson'">
        <h2>Add Lesson</h2>
        <form @submit.prevent="addLesson">
          <label>Course ID:</label>
          <input v-model="lesson.course_id" type="text" required />
          
          <label>Material Type:</label>
          <input v-model="lesson.material_type" type="text" required />
          
          <label>Content:</label>
          <textarea v-model="lesson.content" required></textarea>
          
          <button type="submit">Submit</button>
        </form>
      </div>



    </div>
</div>
</template>

<script setup>
import { ref } from "vue";
import ProfessorNavBar from "@/components/Professor/ProfessorNavBar.vue";
import axios from "axios";

const activeComponent = ref("");
const professordetails = ref("");
const coursedetails = ref(null);
const queries = ref([]);
const pendingInstructors = ref([]);
const lesson = ref({ course_id: "", material_type: "", content: "" });

const setActiveComponent = (component) => {
  activeComponent.value = component;
  if (component === "TopQueries") fetchTopQueries();
  if (component == "ProfessorDetails") fetchProfessorDetails();
  if (component === "CourseDetails") fetchCourseDetails();
  if (component === "PendingInstructors") fetchPendingInstructors();
};


const fetchTopQueries = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/topquery",
    {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    queries.value = response.data;
  } catch (error) {
    console.error("Error fetching queries:", error);
  }
};

const fetchCourseDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_courses", {
      headers: { Authorization: `Bearer ${token}` },
    });
    coursedetails.value = response.data.courses || [];
    console.log(coursedetails);
  } catch (error) {
    console.error("Error fetching course details:", error);
  }
};

const fetchProfessorDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/professor_details", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // console.log(response.data);
    professordetails.value = response.data; // Adjust according to API response structure
    // console.log(professordetails);
  } catch (error) {
    console.error("Error fetching admin details:", error);
  }
};

const fetchPendingInstructors = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/pending_instructor", {
      headers: { Authorization: `Bearer ${token}` },
    });
    pendingInstructors.value = response.data;
    console.log(response.data);
  } catch (error) {
    console.error("Error fetching pending instructors:", error);
  }
};

const approveInstructor = async (requestId, status) => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.put(`http://127.0.0.1:5000/approve_instructor/${requestId}`, 
      { status: status },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log(response.data);
    fetchPendingInstructors(); // Refresh the list after approval/rejection
  } catch (error) {
    console.error(`Error approving instructor (${status}):`, error);
  }
};

const addLesson = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.post("http://127.0.0.1:5000/add_suplementary", lesson.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log(response.data);
    alert("Lesson added successfully!");
    lesson.value = { course_id: "", material_type: "", content: "" }; // Reset form
  } catch (error) {
    console.error("Error adding lesson:", error);
  }
};


</script>

<style scoped>
.container {
  display: flex;
  max-width: 1000px;
  margin: auto;
}

.sidebar {
  width: 250px;
  padding: 20px;
  background: #f4f4f4;
  border-right: 1px solid #ddd;
}

button {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border: none;
  background: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.content {
  flex-grow: 1;
  padding: 20px;
}

input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>

