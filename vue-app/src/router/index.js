import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import('../views/Map.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/comparison',
    name: 'Comparison',
    component: () => import('../views/Comparison.vue'),
    meta: { keepAlive: false }
  },
  {
    path: '/trends',
    name: 'Trends',
    component: () => import('../views/Trends.vue'),
    meta: { keepAlive: false }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/country/:name',
    name: 'CountryDetail',
    component: () => import('../views/CountryDetail.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 