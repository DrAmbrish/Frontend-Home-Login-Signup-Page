<template>
  <InstructorNavBar/>
  <div class="add-live-session-container">
    <label>Schedule Live Session</label>
    <br>

    <form @submit.prevent="saveLiveSession" class="live-session-form">
      <div class="form-group">
        <label for="courseId">Course ID</label>
        <input
            type="number"
            id="courseId"
            v-model.number="courseId"
            placeholder="Enter Course ID"
            min=""
            required
        >
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
            id="description"
            v-model="liveSession.description"
            placeholder="Enter session description and what students will learn"
            rows="4"
            required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="ytLink">YouTube Live Link</label>
        <input
            type="url"
            id="ytLink"
            v-model="liveSession.yt_link"
            placeholder="Enter YouTube live stream link"
            required
        >
      </div>

      <div class="form-actions">
        <button type="button" @click="clearForm" class="cancel-button">Cancel</button>
        <button
            type="submit"
            class="save-button"
            :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Scheduling...' : 'Schedule Session' }}
        </button>
      </div>
    </form>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
import axios from 'axios';

export default {
  name: 'AddLiveSession',
  components: {
    InstructorNavBar
  },
  setup() {
    const courseId = ref(1);
    const liveSession = ref({
      description: '',
      yt_link: ''
    });
    const isSubmitting = ref(false);
    const errorMessage = ref('');

    const saveLiveSession = async () => {
      // Reset error message
      errorMessage.value = '';

      // Validate input
      if (!courseId.value || !liveSession.value.description || !liveSession.value.yt_link) {
        errorMessage.value = 'Please fill in all fields.';
        return;
      }

      // Check for access token
      const token = localStorage.getItem('access_token');
      if (!token) {
        errorMessage.value = 'Unauthorized: No access token found.';
        return;
      }

      // Set submitting state
      isSubmitting.value = true;

      try {
        // Make API call to create live session
        const response = await axios.post(
            `http://127.0.0.1:5000/add_livesession`,
            {
              course_id: courseId.value,
              description: liveSession.value.description,
              yt_link: liveSession.value.yt_link
            },
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
        );
        console.log(response)

        // Show success alert
        alert('Live session added successfully!');

        // Clear form
        clearForm();
      } catch (error) {
        console.error('Failed to schedule live session:', error);

        // Set error message
        errorMessage.value = error.response?.data?.message || 'Failed to schedule live session.';
      } finally {
        isSubmitting.value = false;
      }
    };

    const clearForm = () => {
      courseId.value = 1;
      liveSession.value = {
        description: '',
        yt_link: ''
      };
      errorMessage.value = '';
    };

    return {
      courseId,
      liveSession,
      isSubmitting,
      errorMessage,
      saveLiveSession,
      clearForm
    };
  }
}
</script>

<style scoped>
.add-live-session-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.live-session-form {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, textarea, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-button, .save-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button {
  background-color: #f1f1f1;
  color: #333;
}

.cancel-button:hover {
  background-color: #e1e1e1;
}

.save-button {
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  color: white;
}

.save-button:hover {
  background-color: #2980b9;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #d4edda;
  color: #155724;
  border-radius: 4px;
  text-align: center;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>