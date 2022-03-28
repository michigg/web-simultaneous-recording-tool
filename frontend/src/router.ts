import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Test from './modules/audioTesting/pages/Test.vue'

const mainRoutes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Test',
    component: Test,
  },
]
const routes = [...mainRoutes]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
