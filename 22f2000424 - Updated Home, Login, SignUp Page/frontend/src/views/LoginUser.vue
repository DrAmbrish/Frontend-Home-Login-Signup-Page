<template>
    <nav>
      <router-link to="/signup">Signup</router-link> |
      <router-link to="/login">Login</router-link>     
    </nav>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="loginUser">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" >
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" >
            </div>
            <button type="submit">Login</button>
        </form>
        
    </div>
</template>





<style scoped>
.login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 30px;
    border-radius: 15px;
    background: linear-gradient(135deg, #ffffff, #f3f4f6);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    color: #333;
}

h2 {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 20px;
    color: #222;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
    color: #555;
}

.form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    background: #fff;
    color: #333;
    transition: border-color 0.3s ease;
}

.form-group input:focus {
    border-color: #007bff;
    box-shadow: 0 0 8px rgba(0, 123, 255, 0.3);
    outline: none;
}

button {
    width: 100%;
    padding: 12px;
    background: #007bff;
    color: #fff;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s ease-in-out;
}

button:hover {
    background: #0056b3;
    transform: scale(1.02);
}

.error-message {
    margin-top: 20px;
    padding: 10px;
    background: rgba(255, 77, 79, 0.1);
    color: #ff4d4f;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
}

@media (max-width: 768px) {
    .login-container {
        padding: 20px;
    }

    button {
        font-size: 0.9rem;
    }
}
</style>
