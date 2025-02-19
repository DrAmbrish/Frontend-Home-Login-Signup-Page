<template>
  
    <router-link to="/"></router-link> 

    <h1>AI Agent for Academic Guidance</h1>
    <h3>By Team - 16 (Jan 2025)</h3>

    <h3>Welcome To Software Engineering Project</h3>
    
      
  
  <router-view/>
</template>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

body {
  background-color: #f9f9fb;
  color: #333;
}

h1{
  padding: 1rem;
}
h3{
  padding: 1rem;
}
nav {
  background-color: #e3f2fd;
  padding: 1rem;
}

nav ul {
  list-style: none;
  display: flex;
  justify-content: flex-end;
}

nav li {
  margin-left: 1rem;
}

nav button {
  background-color: #fff;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

nav button:hover {
  background-color: #cce4f6;
  color: #0056b3;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

</style>
