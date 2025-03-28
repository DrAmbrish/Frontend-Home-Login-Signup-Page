<template>
  <AdminNavBar />
  <div class="container">
    <div class="sidebar">
      <button @click="setActiveComponent('AdminDetails')">Admin Details</button>
      <button @click="setActiveComponent('StudentDetails')">Student Details</button>
      <button @click="setActiveComponent('CourseDetails')">Course Details</button>
      <button @click="setActiveComponent('TopQueries')">Top Queries</button>
      <!-- <button @click="setActiveComponent('QueryDetails')">Query Details</button> -->
      <!-- <button @click="setActiveComponent('SolveQuery')">Solve Query</button> -->
      <button @click="setActiveComponent('AddCourse')">Add Course</button>
      <button @click="setActiveComponent('EditCourse')">Edit Course</button>
      <button @click="setActiveComponent('AddCourseMaterial')">Add Course Material</button>
      <button @click="setActiveComponent('EditCourseMaterial')">Edit Course Material</button>
      <button @click="setActiveComponent('AssignCourse')">Assign Course</button>
    </div>

    <div class="content">
      <div v-if="activeComponent === 'AdminDetails'">
        <h2>Admin Details</h2>
        <ul v-if="admindetails">
          <li><strong>Name:</strong> {{ admindetails.name }}</li>
          <li><strong>Email:</strong> {{ admindetails.email }}</li>
          <li><strong>Role:</strong> {{ admindetails.role }}</li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

       <!-- Student Details -->
       <div v-if="activeComponent === 'StudentDetails'">
      <h2>Student Details</h2>
      <ul v-if="studentdetails.length">
        <li v-for="student in studentdetails" :key="student.id">
          <strong>Name:</strong> {{ student.name }} <br />
          <strong>Email:</strong> {{ student.email }} <br />
          <strong>Total Courses:</strong> {{ student.total_courses }} <br />
          <strong>Created At:</strong> {{ student.created_at }}
        </li>
      </ul>
      <p v-else>No student details found.</p>
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

      <div v-if="activeComponent === 'TopQueries'">
        <h2>Top Support Queries</h2>
        <ul v-if="queries.length">
          <li v-for="query in queries" :key="query.query">
            {{ query.query_text }} - {{ query.count }} times
          </li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

      <div v-if="activeComponent === 'QueryDetails'">
        <h2>Query Details</h2>
        <input v-model="queryId" type="number" placeholder="Enter Query ID" />
        <button @click="fetchQueryDetails">Fetch Details</button>
        <p v-if="queryDetails">{{ queryDetails }}</p>
      </div>

      <div v-if="activeComponent === 'SolveQuery'">
        <h2>Solve Query</h2>
        <input v-model="queryId" type="number" placeholder="Enter Query ID" />
        <button @click="solveQuery">Mark as Solved</button>
        <p v-if="solveMessage">{{ solveMessage }}</p>
      </div>

      <div v-if="activeComponent === 'AddCourse'">
        <h2>Add Course</h2>
        <input v-model="course.name" placeholder="Course Name" />
        <input v-model="course.description" placeholder="Course Description" />
        <button @click="addCourse">Add</button>
      </div>

      <div v-if="activeComponent === 'EditCourse'">
        <h2>Edit Course</h2>
        <input v-model="courseId" type="number" placeholder="Enter Course ID" />
        <input v-model="course.name" placeholder="New Name" />
        <input v-model="course.description" placeholder="New Description" />
        <button @click="editCourse">Edit</button>
      </div>

    <div v-if="activeComponent === 'AddCourseMaterial'">
    <h2>Add Course Material</h2>
    <input v-model="courseId" type="number" placeholder="Course ID" />
    <input v-model="material.week_number" type="number" placeholder="Week Number" />
    <input v-model="material.title" placeholder="Material Title" />
    <input v-model="material.material_link" placeholder="Material Link" />
    <button @click="addCourseMaterial">Add</button>
  </div>

      <div v-if="activeComponent === 'EditCourseMaterial'">
        <h2>Edit Course Material</h2>
        <input v-model="materialId" type="number" placeholder="Material ID" />
        <input v-model="material.title" placeholder="New Title" />
        <input v-model="material.link" placeholder="New Link" />
        <button @click="editCourseMaterial">Edit</button>
      </div>

      <div v-if="activeComponent === 'AssignCourse'">
        <h2>Assign Course</h2>
        <input v-model="courseId" type="number" placeholder="Course ID" />
        <input v-model="studentId" type="number" placeholder="Student ID" />
        <button @click="assignCourse">Assign</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import AdminNavBar from "@/components/Admin/AdminNavBar.vue";
import axios from "axios";

const activeComponent = ref("");
const admindetails = ref("");
const studentdetails = ref(null);
const coursedetails = ref(null);
const queries = ref([]);
const queryId = ref(null);
const queryDetails = ref("");
const solveMessage = ref("");
const course = ref({ name: "", description: "" });
const courseId = ref(null);
const studentId = ref(null);
const material = ref({ week_number: "", title: "", material_link: "" });
const materialId = ref(null);

const setActiveComponent = (component) => {
  activeComponent.value = component;
  if (component === "TopQueries") fetchTopQueries();
  if (component == "AdminDetails") fetchAdminDetails();
  if (component === "StudentDetails") fetchStudentDetails();
  if (component === "CourseDetails") fetchCourseDetails();
};


const fetchStudentDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_students", {
      headers: { Authorization: `Bearer ${token}` },
    });
    studentdetails.value = response.data.students || [];
    console.log(studentdetails);
  } catch (error) {
    console.error("Error fetching student details:", error);
  }
};

// Fetch Course Details
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

const fetchAdminDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_details", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // console.log(response.data);
    admindetails.value = response.data; // Adjust according to API response structure
    // console.log(admindetails);
  } catch (error) {
    console.error("Error fetching admin details:", error);
  }
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
    console.log(queries);
  } catch (error) {
    console.error("Error fetching queries:", error);
  }
};

const fetchQueryDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get(`http://127.0.0.1:5000/query_detail/${queryId.value}`,
    {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    queryDetails.value = response.data.details;
  } catch (error) {
    console.error("Error fetching query details:", error);
  }
};

const solveQuery = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.post(`http://127.0.0.1:5000/solve_query/${queryId.value}`,
    {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    solveMessage.value = "Query marked as solved!";
  } catch (error) {
    console.error("Error solving query:", error);
  }
};

const addCourse = async () => {
  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const payload = {
      name: course.value.name?.toString().trim() || "",
      description: course.value.description?.toString().trim() || ""
    };

    console.log("Sending Payload:", payload); // Debugging step

    const response = await axios.post(
      "http://127.0.0.1:5000/add_course",
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert("Course added successfully!");
  } catch (error) {
    console.error("Error adding course:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to add course.");
  }
};


const editCourse = async () => {
  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const response = await axios.put(
      `http://127.0.0.1:5000/edit_course/${courseId.value}`,
      course.value,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert("Course updated successfully!");
  } catch (error) {
    console.error("Error editing course:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to edit course.");
  }
};


const addCourseMaterial = async () => {
  if (!courseId.value || !material.value.week_number || !material.value.title || !material.value.material_link) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const response = await axios.post(
      `http://127.0.0.1:5000/add_course/${courseId.value}/material`,
      material.value,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert("Material added successfully!");

    // Reset input fields after successful submission
    material.value = { week_number: "", title: "", material_link: "" };
  } catch (error) {
    console.error("Error adding material:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to add material.");
  }
};



const editCourseMaterial = async () => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.put(`http://127.0.0.1:5000/edit_course/material/${materialId.value}`, material.value,
    {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    alert("Material updated successfully!");
  } catch (error) {
    console.error("Error editing material:", error);
  }
};

const assignCourse = async () => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.post(
      `http://127.0.0.1:5000/assign-course/${courseId.value}/${studentId.value}`, 
      {}, // Empty body
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    alert("Course assigned successfully!");
  } catch (error) {
    console.error("Error assigning course:", error);
    alert("Failed to assign course. Please check permissions.");
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
