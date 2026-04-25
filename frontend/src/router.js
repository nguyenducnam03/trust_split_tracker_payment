import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from './services/auth'
import CreateSession from './components/CreateSession.vue'
import SessionDetail from './components/SessionDetail.vue'
import ConfirmPayment from './components/ConfirmPayment.vue'
import Login from './components/Login.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login },
    { path: '/', component: CreateSession, meta: { requiresAuth: true } },
    { path: '/sessions/:id', component: SessionDetail, meta: { requiresAuth: true } },
    { path: '/pay/:id', component: ConfirmPayment },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isLoggedIn()) {
    return '/login'
  }
})

export default router
