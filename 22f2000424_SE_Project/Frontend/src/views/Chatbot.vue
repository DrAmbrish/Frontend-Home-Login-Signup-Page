<template>
  <div class="chatbot-container">
    <div class="chatbot-card">
      <div class="chat-header">
        <h2>Chatbot Assistant</h2>
        <p>Use the chatbot to get responses or answers of technical questions.</p>
      </div>
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
          <div class="message-content">
            <p v-html="formatMessage(message.text)"></p>
          </div>
          <div v-if="message.sender === 'chatbot'" class="message-actions">
            <button @click="copyToResponse(message.text)" class="copy-button">Copy Response</button>
          </div>
        </div>
        <!-- Loading Animation -->
        <div v-if="isLoading" class="message chatbot loading-message">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <textarea v-model="newMessage" placeholder="Type your message here..." @keydown.enter.prevent="sendMessage"
                  rows="3"></textarea>
        <button @click="sendMessage" :disabled="!newMessage.trim() || isLoading" class="send-button">
          <span v-if="!isLoading"></span>
          <span v-else class="send-loading"></span>
        </button>
      </div>
      <div v-if="queryInfo" class="query-context">
        <h3>Current Query Context</h3>
        <div class="query-context-info">
          <p><strong>Query ID:</strong> {{ queryInfo.id }}</p>
          <p><strong>Subject:</strong> {{ queryInfo.subject }}</p>
        </div>
        <button @click="goToQueryDetails" class="context-action-button">
          Go to Query Details
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chatbot',
  data() {
    return {
      messages: [
        {
          sender: 'chatbot',
          text: 'Hello! I\'m your AI assistant. How can I help you ?'
        }
      ],
      newMessage: '',
      queryInfo: null,
      isLoading: false,
      apiUrl: 'http://127.0.0.1:5000/chat' // API endpoint for chat service
    }
  },
  mounted() {
    // Check if we have pre-filled message from query details
    const prefill = this.$route.query.prefill
    const queryId = this.$route.query.queryId
    if (prefill) {
      this.newMessage = prefill
      // Fetch query details if
      if (queryId) {
        this.fetchQueryInfo(queryId)
      }
    }
    this.scrollToBottom()
  },
  updated() {
    this.scrollToBottom()
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim() || this.isLoading) return

      // Add user message
      this.messages.push({
        sender: 'user',
        text: this.newMessage
      })
      const userMessage = this.newMessage
      this.newMessage = ''

      // Show loading animation
      this.isLoading = true

      try {
        // Call the chatbot API
        const token = localStorage.getItem("access_token");
        const response = await fetch(this.apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', "Authorization": `Bearer ${token}` },
          body: JSON.stringify({ query: userMessage })
        });

        if (response.ok) {
          const data = await response.json();
          this.messages.push({
            sender: 'chatbot',
            text: data.response || 'I understand your message. How can I assist further?'
          });
        } else {
          // Handle error response
          this.messages.push({
            sender: 'chatbot',
            text: 'Sorry, I encountered an error processing your request. Please try again later.'
          });
        }
      } catch (error) {
        // Handle network or other errors
        console.error('Chat API error:', error);
        this.messages.push({
          sender: 'chatbot',
          text: 'Error: Unable to connect to the server. Please check your connection and try again.'
        });
      } finally {
        this.isLoading = false;
      }
    },

    formatMessage(text) {
      // Format code blocks, links, etc.
      return text
          // Replace URLs with clickable links
          .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      // Other formatting could be added here
    },

    copyToResponse(text) {
      // Strip HTML tags to get plain text
      const plainText = text.replace(/<[^>]*>/g, '');

      // Copy to clipboard
      navigator.clipboard.writeText(plainText).then(() => {
        alert("Copied to clipboard!"); // Optional: Show confirmation
      }).catch(err => {
        console.error("Failed to copy: ", err);
      });

      // Emit event for parent component if needed
      this.$emit('use-response', plainText);

      // Navigate to another view with the copied response
      this.$router.push({
        name: 'query-response',
        query: {
          responseText: plainText,
          queryId: this.queryInfo ? this.queryInfo.id : null
        }
      }).catch(err => console.warn("Navigation error: ", err));
    },

    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight
      }
    },

    fetchQueryInfo(queryId) {
      // In a real app, this would be an API call
      // For now, simulate with dummy data
      setTimeout(() => {
        this.queryInfo = {
          id: queryId,
          subject: 'Technical Support Request #' + queryId,
          // Other query details could be added here
        }
      }, 500)
    },

    goToQueryDetails() {
      if (this.queryInfo) {
        this.$router.push({
          name: 'QueryDetails',
          params: {id: this.queryInfo.id}
        })
      }
    }
  }
}
</script>

<style scoped>
/* General container styles */
.chatbot-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Inter', 'Segoe UI', Roboto, -apple-system, sans-serif;
}

/* Chatbot card */
.chatbot-card {
  border: 1px solid #dcdfe4;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 600px;
  
}

/* Header styles */
.chat-header {
  padding: 16px;
  background: linear-gradient(to right,rgb(186, 230, 250),rgb(247, 146, 242));
  border-bottom: 1px solid #e5e5e5;  
}

.chat-header h2 {
  margin: 0;
  font-size: 1.1rem;  
  color: #222;
  font-weight: 500;
}

.chat-header p {
  margin: 4px 0 0;
  font-size: 0.9rem;
  color: #222;
  font-weight: 500;
}

/* Chat messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #fafafa;  
  gap: 12px;
  display: flex;
  flex-direction: column;
}

.chat-messages::-webkit-scrollbar {
  width: 5px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #c4c4c4;  
  border-radius: 8px;
}

/* User message */
.message {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 0.95rem;
  line-height: 1.4;
  word-break: break-word;
  animation: messageAppear 0.3s ease-out;
}

.message.user {
  align-self: flex-end;
  background-color: #1a73e8;
  color: #fff;
  border-bottom-right-radius: 4px;
}

/* Chatbot message */
.message.chatbot {
  align-self: flex-start;
  /*background-color: #f4f4f4;*/
  background-color:rgb(235, 243, 250);
  box-shadow: 0 5px 5px rgba(135, 194, 247, 0.6);
  color: #333;
  border: 1px solid #e5e5e5;
  border-bottom-left-radius: 4px;
}


/* Message appearance animation */
@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Chat input */
.chat-input {
  padding: 12px;
  border-top: 1px solid #e5e5e5;
  background-color: #ffffff;
  display: flex;
  gap: 8px;
}

.chat-input textarea {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #dcdfe4;
  border-radius: 20px;
  font-size: 0.95rem;
  background-color: #fafafa;
  transition: border-color 0.2s;
}

.chat-input textarea:focus {
  outline: none;
  border-color: #1a73e8;
  box-shadow: 0 6px 6px rgba(245, 103, 210, 0.8);
}

.send-button {
  background-color:rgb(142, 191, 255);
  color: #ffffff;
  border: none;
  border-radius: 20px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.send-button:hover {
  background-color:rgb(36, 121, 248);
  box-shadow: 0 6px 6px rgba(117, 137, 250, 0.8);
}

.send-button:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

/* Query context */
.query-context {
  padding: 12px;
  border-top: 1px solid #e5e5e5;
  background-color: #f7f7f7;
}

.query-context h3 {
  margin: 0 0 8px;
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
}

.query-context-info {
  padding: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  font-size: 0.875rem;
  color: #555;
}

/* Copy button */
.copy-button {
  /*background-color: #ffffff;*/
  background-color: transparent;
  border: 1px solidrgb(239, 243, 250);
  padding: 6px 12px;
  font-size: 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  color: #222;
  transition: background-color 0.2s;
}

.copy-button:hover {
  background-color:rgb(188, 222, 250);
}

.copy-button:active {
  background-color:rgb(138, 197, 252);
}

.message-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
  /*opacity: 0;*/
  transition: opacity 0.2s ease;
  color: #222;
}

.message:hover .message-actions {
  opacity: 1;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: #c4c4c4;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.3s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.15s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Message content formatting */
.message-content p {
  margin: 0;
}

.message-content code {
  background-color: #f4f4f4;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  font-size: 0.85rem;
}

.message-content pre {
  background-color: #2b2b2b;
  color: #f8f8f8;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.85rem;
}
</style>
