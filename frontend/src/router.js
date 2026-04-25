import { createRouter, createWebHistory } from 'vue-router'
import CreateSession from './components/CreateSession.vue'
import SessionDetail from './components/SessionDetail.vue'
import ConfirmPayment from './components/ConfirmPayment.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: CreateSession },
    { path: '/sessions/:id', component: SessionDetail },
    { path: '/pay/:id', component: ConfirmPayment },
  ],
})
