<template>
  <InstructorNavBar/>
  <div class="add-assignment-container">
    <h1>Add Assignment</h1>

    <form @submit.prevent="saveAssignment" class="assignment-form">
      <div class="form-group">
        <label for="title">Assignment Title</label>
        <input
            type="text"
            id="title"
            v-model="assignment.title"
            placeholder="Enter assignment title"
            required
        >
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
            id="description"
            v-model="assignment.description"
            placeholder="Enter assignment description and instructions"
            rows="5"
            required
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="type">Assignment Type</label>
          <select id="type" v-model="assignment.type" required>
            <option value="">Select type</option>
            <option value="graded">Graded Assignment (GA)</option>
            <option value="practice">Practice Assignment</option>
          </select>
        </div>

        <div class="form-group">
          <label for="deadline">Deadline</label>
          <input
              type="datetime-local"
              id="deadline"
              v-model="assignment.deadline"
              required
          >
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="points">Total Points</label>
          <input
              type="number"
              id="points"
              v-model="assignment.points"
              min="0"
              step="1"
              required
          >
        </div>

        <div class="form-group">
          <label for="category">Category</label>
          <select id="category" v-model="assignment.category" required>
            <option value="">Select a category</option>
            <option value="frontend">Frontend Development</option>
            <option value="backend">Backend Development</option>
            <option value="database">Database</option>
            <option value="devops">DevOps</option>
            <option value="mobile">Mobile Development</option>
            <option value="design">UI/UX Design</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="link">Assignment Link</label>
        <input
            type="url"
            id="link"
            v-model="assignment.link"
            placeholder="Enter link to assignment details/submission"
        >
      </div>

      <div class="form-group">
        <label for="resources">Additional Resources (Optional)</label>
        <textarea
            id="resources"
            v-model="assignment.resources"
            placeholder="Enter links to helpful resources, one per line"
            rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="button" @click="clearForm" class="cancel-button">Cancel</button>
        <button type="submit" class="save-button">Save Assignment</button>
      </div>
    </form>

    <div v-if="showSuccess" class="success-message">
      Assignment has been successfully added!
    </div>
  </div>
</template>

<script>
import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
export default {
  name: 'AddAssignment',
  components: {
    InstructorNavBar
  },
  data() {
    return {
      assignment: {
        title: '',
        description: '',
        type: '',
        deadline: '',
        points: '',
        category: '',
        link: '',
        resources: ''
      },
      showSuccess: false
    }
  },
  methods: {
    saveAssignment() {
      // In a real app, this would call an API
      // For demo, we'll just show a success message
      console.log('Saving assignment:', this.assignment)

      // Show success message
      this.showSuccess = true
      setTimeout(() => {
        this.showSuccess = false
        this.clearForm()
      }, 3000)
    },
    clearForm() {
      this.assignment = {
        title: '',
        description: '',
        type: '',
        deadline: '',
        points: '',
        category: '',
        link: '',
        resources: ''
      }
    }
  }
}
</script>

<style scoped>
.add-assignment-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.assignment-form {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
  background-color: #3498db;
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