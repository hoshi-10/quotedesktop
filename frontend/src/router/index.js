import { createRouter, createWebHistory } from 'vue-router'
import ExcelManager from '../views/ExcelManager.vue'
import ExcelOverview from '../views/ExcelOverview.vue'

const routes = [
  {
    path: '/',
    redirect: '/manager'
  },
  {
    path: '/manager',
    component: ExcelManager
  },
  {
    path: '/overview',
    component: ExcelOverview
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router