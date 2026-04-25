<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-else-if="!session" class="empty">Session not found</div>
  <div v-else class="session-detail">
    <div class="page-header">
      <h2>{{ session.name }}</h2>
      <span class="share-hint">Share link:</span>
      <div class="link-row">
        <input :value="session.share_url" readonly />
        <button class="btn btn-small" @click="copyLink">{{ copied ? 'Copied!' : 'Copy' }}</button>
      </div>
    </div>

    <div class="summary">
      <span>Total: <strong>{{ formatMoney(totalAmount) }}</strong></span>
      <span>{{ confirmedCount }}/{{ session.members.length }} confirmed</span>
    </div>

    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
    </div>

    <table class="grid">
      <thead>
        <tr>
          <th class="col-no">#</th>
          <th class="col-name">Name</th>
          <th class="col-amount">Amount</th>
          <th class="col-status">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, i) in session.members" :key="i" :class="{ confirmed: m.confirmed }">
          <td class="col-no">{{ i + 1 }}</td>
          <td class="col-name">{{ m.name || '—' }}</td>
          <td class="col-amount">{{ formatMoney(m.amount) }}</td>
          <td class="col-status">
            <span v-if="m.confirmed" class="badge badge-confirmed">✓ Paid</span>
            <span v-else class="badge badge-pending">Pending</span>
          </td>
        </tr>
      </tbody>
    </table>

    <router-link to="/" class="back-link">← New session</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSession } from '../services/api'

const route = useRoute()
const session = ref(null)
const loading = ref(true)
const copied = ref(false)
let timer = null

const totalAmount = computed(() =>
  session.value?.members.reduce((s, m) => s + m.amount, 0) ?? 0
)
const confirmedCount = computed(() =>
  session.value?.members.filter(m => m.confirmed).length ?? 0
)
const progressPercent = computed(() => {
  const total = totalAmount.value
  if (!total) return 0
  const paid = session.value.members.filter(m => m.confirmed).reduce((s, m) => s + m.amount, 0)
  return Math.round((paid / total) * 100)
})

async function load() {
  try {
    session.value = await getSession(route.params.id)
  } catch {
    session.value = null
  } finally {
    loading.value = false
  }
}

async function copyLink() {
  await navigator.clipboard.writeText(session.value.share_url)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}

function formatMoney(n) {
  return Math.round(n || 0).toLocaleString('vi-VN') + 'đ'
}

onMounted(() => {
  load()
  timer = setInterval(load, 10000)
})
onUnmounted(() => clearInterval(timer))
</script>
