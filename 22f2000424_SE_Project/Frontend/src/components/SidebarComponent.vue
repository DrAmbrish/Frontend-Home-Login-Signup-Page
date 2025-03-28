<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <!-- Mobile Menu Toggle -->
      <div class="mobile-menu-toggle" @click="toggleMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>

      <!-- Sidebar/Lecture List -->
      <div class="lecture-list" :class="{ 'mobile-active': mobileMenuActive }">
        <div class="mobile-close" @click="toggleMobileMenu">&times;</div>

        <div v-if="loading" class="loading">Loading course...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="selectedCourse">
          <h1>{{ selectedCourse.name }}</h1>

          <!-- Course content -->
          <div>
            <!-- Weekly Materials -->
            <ul v-if="organizedWeeks.length > 0">
              <li v-for="(week, index) in organizedWeeks" :key="index">
                <h3 @click="toggleWeek(index)">
                  Week {{ week.weekNumber }}
                  <span>{{ expandedWeek === index ? '▲' : '▼' }}</span>
                </h3>
                <ul v-show="expandedWeek === index">
                  <li v-if="week.materials.length === 0" class="no-content">No materials available for this week</li>
                  <li
                      v-for="(material, idx) in week.materials"
                      :key="idx"
                      @click="selectContent(material.video_link, null, idx, index)"
                      :class="{ 'selected': selectedLecture === idx && currentWeek === index && !viewingSupplementary }"
                  >
                    <span v-if="selectedLecture === idx && currentWeek === index && !viewingSupplementary" class="dot"></span>
                    {{ material.title }}
                  </li>

                  <!-- Live Sessions -->
                  <li v-if="week.liveSessions.length === 0 && week.materials.length > 0" class="no-content">No live sessions for this week</li>
                  <li
                      v-for="(session, sessionIdx) in week.liveSessions"
                      :key="`session-${sessionIdx}`"
                      @click="selectContent(session.yt_link, null, `session-${sessionIdx}`, index)"
                      :class="{ 'selected': selectedLecture === `session-${sessionIdx}` && currentWeek === index && !viewingSupplementary }"
                  >
                    <span v-if="selectedLecture === `session-${sessionIdx}` && currentWeek === index && !viewingSupplementary" class="dot"></span>
                    Live Session: {{ session.description }}
                  </li>
                </ul>
              </li>
            </ul>
            <div v-else class="no-data">No weekly content available for this course.</div>

            <!-- Supplementary Content -->
            <br>
            <h3 @click="toggleSupplementary">
              Supplementary Content
              <span>{{ showSupplementary ? '▲' : '▼' }}</span>
            </h3>
            <ul v-show="showSupplementary">
              <li v-if="!selectedCourse.supplementary_materials || selectedCourse.supplementary_materials.length === 0" class="no-content">
                No supplementary content available for this course
              </li>
              <li
                  v-else
                  v-for="(material, idx) in selectedCourse.supplementary_materials"
                  :key="idx"
                  @click="selectSupplementaryContent(material.content, idx); toggleMobileMenuIfActive();"
                  :class="{ 'selected': selectedSupplementary === idx && viewingSupplementary }"
              >
                <span v-if="selectedSupplementary === idx && viewingSupplementary" class="dot"></span>
                {{ material.material_type }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <div class="content-area">
        <!-- Error Messages -->
        <div class="content-error" v-if="contentError">
          <h3>{{ contentError }}</h3>
          <p>Please select another item or contact support if this issue persists.</p>
        </div>
        <!-- Video Player, PDF Viewer or Default Page Section -->
        <div class="video-player" v-else-if="selectedVideoUrl && !viewingSupplementary">
          <VideoPlayerComponent :videoSrc="selectedVideoUrl" @error="handleContentError"/>
        </div>
        <div class="pdf-viewer" v-else-if="selectedPdfUrl && viewingSupplementary">
          <PDFViewerComponent :pdfSrc="selectedPdfUrl" @error="handleContentError"/>
        </div>
        <div class="default-page" v-else>
          <div class="welcome-container">
            <h3>Welcome to {{ selectedCourse ? selectedCourse.name : 'Course' }}</h3>
            <p v-if="selectedCourse">Select a lecture or supplementary content from the list to start learning!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VideoPlayerComponent from './VideoPlayerComponent.vue';
import PDFViewerComponent from './PDFViewerComponent.vue';
import axios from 'axios';

export default {
  components: {
    VideoPlayerComponent,
    PDFViewerComponent,
  },
  data() {
    return {
      loading: true,
      error: null,
      contentError: null,
      selectedCourse: null,
      expandedWeek: null,
      selectedVideoUrl: null,
      selectedPdfUrl: null,
      selectedLecture: null,
      selectedSupplementary: null,
      currentWeek: null,
      showSupplementary: false,
      viewingSupplementary: false,
      mobileMenuActive: false,
    };
  },
  computed: {
    organizedWeeks() {
      if (!this.selectedCourse) return [];

      // Check if the required arrays exist
      const materials = this.selectedCourse.materials || [];
      const liveSessions = this.selectedCourse.live_sessions || [];

      // Get all unique week numbers from materials
      const weekNumbers = [...new Set(
          materials.map(m => m.week_number)
      )].sort((a, b) => a - b);

      // Organize content by week
      return weekNumbers.map(weekNumber => {
        return {
          weekNumber: weekNumber,
          materials: materials.filter(m => m.week_number === weekNumber),
          liveSessions: liveSessions.filter(session => {
            // Group live sessions with the closest week
            try {
              if (!session.created_at) return false;

              const sessionDate = new Date(session.created_at);
              const weekMaterials = materials.filter(m => m.week_number === weekNumber);

              if (weekMaterials.length === 0) return false;

              if (!weekMaterials[0].created_at) return false;

              const weekStartDate = new Date(weekMaterials[0].created_at);
              const nextWeekNumber = weekNumbers[weekNumbers.indexOf(weekNumber) + 1];
              const nextWeekMaterials = nextWeekNumber
                  ? materials.filter(m => m.week_number === nextWeekNumber)
                  : [];
              const nextWeekStartDate = nextWeekMaterials.length > 0 && nextWeekMaterials[0].created_at
                  ? new Date(nextWeekMaterials[0].created_at)
                  : new Date(8640000000000000); // Max date

              return sessionDate >= weekStartDate && sessionDate < nextWeekStartDate;
            } catch (error) {
              console.error('Error processing live session date:', error);
              return false;
            }
          })
        };
      });
    }
  },
  created() {
    // Fetch course details when component is created
    this.fetchCourseDetails();
  },
  methods: {
    async fetchCourseDetails() {
      try {
        this.loading = true;
        this.error = null;

        // Get the course ID from the route
        const courseId = this.$route.params.id;

        // Get the JWT token from localStorage
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "No access token found. Please log in again.";
          this.loading = false;
          return;
        }

        // Set up headers with the JWT token
        const headers = {
          Authorization: `Bearer ${token}`
        };

        // Fetch course details
        const response = await axios.get(`http://localhost:5000/course/${courseId}`, { headers });

        // Extract course data from the response
        if (response.data && response.data.course_data) {
          this.selectedCourse = response.data.course_data;
        } else {
          throw new Error('Invalid course data format');
        }

        this.loading = false;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Your session has expired. Please log in again.';
          // Redirect to login page
          this.$router.push('/login');
        } else {
          this.error = 'Failed to load course details. Please try again later.';
        }
        this.loading = false;
        console.error('Error fetching course details:', error);
      }
    },
    toggleWeek(index) {
      // If clicking the already expanded week, close it
      if (this.expandedWeek === index) {
        this.expandedWeek = null;
      } else {
        // Otherwise, open the clicked week and close supplementary
        this.expandedWeek = index;
        this.showSupplementary = false;
      }
    },
    toggleSupplementary() {
      // Toggle supplementary and close any open week
      this.showSupplementary = !this.showSupplementary;
      if (this.showSupplementary) {
        this.expandedWeek = null;
      }
    },
    toggleMobileMenu() {
      this.mobileMenuActive = !this.mobileMenuActive;
    },
    toggleMobileMenuIfActive() {
      // Close menu on selection for mobile devices
      if (window.innerWidth <= 768 && this.mobileMenuActive) {
        this.mobileMenuActive = false;
      }
    },
    selectContent(videoUrl, pdfUrl, idx, weekIndex) {
      // Clear any previous errors
      this.contentError = null;

      // Check if videoUrl is valid
      if (!videoUrl) {
        this.contentError = "Video content is unavailable";
        this.selectedVideoUrl = null;
      } else {
        this.selectedVideoUrl = videoUrl;
      }

      this.selectedPdfUrl = null;
      this.selectedLecture = idx;
      this.currentWeek = weekIndex;
      this.viewingSupplementary = false;
      this.toggleMobileMenuIfActive();
    },
    selectSupplementaryContent(content, idx) {
      // Clear any previous errors
      this.contentError = null;

      // Check if content is valid
      if (!content) {
        this.contentError = "Supplementary content is unavailable";
        this.selectedPdfUrl = null;
      } else {
        this.selectedPdfUrl = content;
      }

      this.selectedVideoUrl = null;
      this.selectedSupplementary = idx;
      this.viewingSupplementary = true;
      this.toggleMobileMenuIfActive();
    },
    handleContentError(message) {
      this.contentError = message || "Content failed to load";
    }
  },
};
</script>


<style scoped>
/* Global Styles */

.default-page {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.welcome-container {
  text-align: center;
}

.default-page h3 {
  color: #333;
  font-size: 28px;
  margin-bottom: 25px;
}

.default-page p {
  font-size: 18px;
  color: #777;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

h1 {
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 25px;
  background: linear-gradient(to right,rgb(250, 60, 148),rgb(177, 68, 219));
  box-shadow: 0 5px 5px rgba(245, 103, 238, 0.68);
  color:  #ffffff;
  border-radius: 15px;
}

h2, h3 {
  font-family: 'Arial', sans-serif;
  color: #333;
  text-align: center;
  border-radius: 18px;
  background: linear-gradient(135deg, #ffffff, #f3f4f6);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

h3 {
  transition: all 0.3s ease;
}

h3:hover {
  color:rgb(143, 7, 102); 
  transform: scale(1.08);
}

.no-data,
.sidebar {
  display: flex;
  width: 100%;
  height: 90%;
  background: #f4f6f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}


.sidebar-content {
  display: flex;
  width: 100%;
  position: relative;
}

.nav-item {
  color: #1d1c1c;
  text-decoration: none;
  font-size: 1rem;
  padding: 8px 16px;
  border-radius: 4px;
  background-color: #ded4cf; /* Medium green */
  transition: background-color 0.3s;
  margin-left: 60px;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
  cursor: pointer;
  
}

.mobile-menu-toggle span {
  display: block;
  height: 3px;
  width: 100%;
  background-color: #333;
  border-radius: 3px;
  
}

.mobile-close {
  display: none;
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  cursor: pointer;
  color: #333;
  
}


.lecture-list {
  width: 300px;
  background: #ffffff;
  padding: 20px;
  border-radius: 18px;
  box-shadow: 0 8px 16px rgba(127, 4, 138, 0.8);
  position: relative;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  cursor: pointer;
  color: #333;
  padding: 10px;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s ease;
 
  background: linear-gradient(135deg, #ffffff, #f3f4f6);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

li:hover {
  color:rgb(143, 7, 102); 
  transform: scale(1.02);
  border-radius: 14px;
}

li.selected {
  background-color: #e3f9e5; /* Light green background when selected */
}

h3 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f4f6f9;
}

h3 span {
  font-size: 18px;
  color:rgb(212, 23, 250);  
}

.content-area {
  flex-grow: 1;
  margin-left: 10px;
  display: flex;
  justify-content: center;  
}

.video-player {
  width: 100%; 
  max-width: 800px; 
  height: 450px; 
  margin: 20px auto;
  border-radius: 12px; 
  box-shadow: 0 4px 12px rgba(57, 14, 214, 0.5); 
  background-color: #000;   
  overflow: hidden;
}

.pdf-viewer {
  width: 100%; 
  max-width: 800px;
  height: 600px; 
  margin: 20px auto;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #f4f4f4; 
  overflow: hidden;
  padding: 10px;
}

iframe, embed {
  width: 100%;
  height: 100%;
  border: none; 
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #28a745; 
  border-radius: 50%;
  margin-right: 10px;
  display: inline-block;
}

.default-page {
  flex-grow: 1;
  text-align: center;
  padding: 100px 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.default-page h3 {
  color: #333;
  font-size: 24px;
}

.default-page p {
  font-size: 18px;
  color: #777;
}

/* Responsive Styles */
@media (max-width: 992px) {
  .sidebar-content {
    flex-direction: column;
  }

  .lecture-list {
    width: 100%;
    margin-bottom: 20px;
  }

  .content-area {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }

  .mobile-close {
    display: block;
  }

  .lecture-list {
    position: fixed;
    top: 0;
    left: -100%;
    width: 80%;
    height: 100%;
    z-index: 1000;
    overflow-y: auto;
    transition: left 0.3s ease;
    padding-top: 50px;
  }

  .lecture-list.mobile-active {
    left: 0;
  }

  .sidebar {
    padding: 10px;
  }

  .sidebar-content {
    padding-top: 40px;
  }

  .video-player, .pdf-viewer, .default-page {
    padding: 15px;
  }

  .default-page {
    padding: 40px 15px;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 20px;
  }

  h3 {
    font-size: 16px;
    padding: 8px;
  }

  li {
    padding: 8px;
    font-size: 14px;
  }
}
</style>

