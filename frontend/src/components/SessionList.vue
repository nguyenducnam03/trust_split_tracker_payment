<template>
  <div class="session-list-page">
    <div class="page-header">
      <h2>My Sessions</h2>
      <router-link to="/create" class="btn-new">+ New Session</router-link>
    </div>

    <p v-if="loading" class="loading">Loading...</p>

    <div v-else-if="sessions.length === 0" class="empty-state">
      <div class="empty-icon">💸</div>
      <p>No sessions yet</p>
      <router-link to="/create" class="btn-submit" style="text-decoration:none; text-align:center">
        Create your first session
      </router-link>
    </div>

    <div v-else class="sessions">
      <router-link
        v-for="s in sessions"
        :key="s.id"
        :to="`/sessions/${s.id}`"
        class="session-card"
      >
        <div class="card-top">
          <span class="card-name">{{ s.name }}</span>
          <span class="card-date">{{ formatDate(s.created_at) }}</span>
        </div>
        <div class="card-bottom">
          <div class="card-progress">
            <div class="card-bar">
              <div class="card-fill" :style="{ width: progress(s) + '%' }"></div>
            </div>
            <span class="card-stat">{{ confirmedCount(s) }}/{{ s.members.length }} paid</span>
          </div>
          <span class="card-amount">{{ formatMoney(totalAmount(s)) }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSessions } from '../services/api'

const sessions = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    sessions.value = await getSessions()
  } finally {
    loading.value = false
  }
})

function confirmedCount(s) {
  return s.members.filter(m => m.confirmed).length
}

function totalAmount(s) {
  return s.members.reduce((sum, m) => sum + m.amount, 0)
}

function progress(s) {
  const total = s.members.length
  if (!total) return 0
  return Math.round((confirmedCount(s) / total) * 100)
}

function formatMoney(n) {
  return Math.round(n || 0).toLocaleString('vi-VN') + 'đ'
}

function formatDate(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
</script>
