<template>

    <nav>
      <router-link to="/signup">Signup</router-link> |
      <router-link to="/login">Login</router-link>     
    </nav>

  <div class="signup-container">
    <h2>Create your Account</h2>
    <form>
      
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username"  />
      </div>
      
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email"  />
      </div>
      
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password"  />
      </div>     
        
      
      

      <router-link to="/login" class="signup-btn">Sign Up</router-link>
    </form>

    <p class="login-link">
        Already have an account?
        <router-link to="/login">Sign in instead</router-link>
      </p>

    
  </div>
</template>


<style scoped>
.signup-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #f5f7fa, #e4e9ee);
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  color: #333;
  overflow-y: auto;
  max-height: 80vh;
}


.signup-container::-webkit-scrollbar {
  width: 8px;
}

.signup-container::-webkit-scrollbar-track {
  background: rgba(200, 200, 200, 0.2);
}

.signup-container::-webkit-scrollbar-thumb {
  background: rgba(100, 100, 100, 0.4);
  border-radius: 10px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #222;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}

input,
textarea,
button {
  width: 100%;
  padding: 12px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  background: #fff;
  color: #333;
}

input:focus,
textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.3);
  outline: none;
}

button {
  background: #007bff;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  border: none;
}

button:hover {
  background: #0056b3;
  transform: scale(1.02);
}


.form-group input[type="file"] {
  background: #fff;
  color: #333;
  border: none;
}


/* Signup Button as a Link */
.signup-btn {
  display: block;
  text-align: center;
  width: 100%;
  padding: 12px;
  background: #1a73e8;
  color: white;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  text-decoration: none;
}

.signup-btn:hover {
  background: #135bb3;
}

 
.login-link {
  margin-top: 20px;
}

.login-link a {
  color: #1a73e8;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}


@media (max-width: 768px) {
  .signup-container {
    padding: 20px;
  }

  input,
  textarea,
  button {
    font-size: 0.9rem;
  }

  h2 {
    font-size: 1.5rem;
  }


 

}
</style>


