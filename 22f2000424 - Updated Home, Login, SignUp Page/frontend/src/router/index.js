import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import SignupUser from '../views/SignupUser.vue'
import LoginUser from '../views/LoginUser.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupUser,
    meta: { requiresGuest: true } 
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser,
    meta: { requiresGuest: true } 
  },
  
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


export default router
