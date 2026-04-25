<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-else-if="!session" class="empty">Session not found</div>
  <div v-else class="session-detail">

    <!-- Header -->
    <div class="sd-header">
      <router-link to="/" class="sd-back">← Back</router-link>
      <h2 class="sd-title">{{ session.name }}</h2>
    </div>

    <!-- Stats -->
    <div class="sd-stats">
      <div class="stat-card">
        <span class="stat-label">Total</span>
        <span class="stat-value">{{ formatMoney(totalAmount) }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Collected</span>
        <span class="stat-value green">{{ formatMoney(paidAmount) }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Confirmed</span>
        <span class="stat-value">{{ confirmedCount }}/{{ session.members.length }}</span>
      </div>
    </div>

    <!-- Progress -->
    <div class="sd-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <span class="progress-label">{{ progressPercent }}%</span>
    </div>

    <!-- Share link -->
    <div class="sd-share">
      <span class="share-label">Share link</span>
      <div class="link-row">
        <input :value="session.share_url" readonly />
        <button class="btn-copy" @click="copyLink">{{ copied ? '✓ Copied' : 'Copy' }}</button>
      </div>
    </div>

    <!-- Members -->
    <div class="sd-members">
      <div
        v-for="(m, i) in session.members"
        :key="i"
        class="member-row"
        :class="{ 'member-paid': m.confirmed }"
      >
        <div class="member-avatar">{{ initials(m.name) }}</div>
        <div class="member-info">
          <span class="member-name">{{ m.name || '—' }}</span>
          <span v-if="m.confirmed" class="member-time">{{ formatTime(m.confirmed_at) }}</span>
        </div>
        <span class="member-amt">{{ formatMoney(m.amount) }}</span>
        <span v-if="m.confirmed" class="badge badge-confirmed">✓ Paid</span>
        <span v-else class="badge badge-pending">Pending</span>
      </div>
    </div>

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
const paidAmount = computed(() =>
  session.value?.members.filter(m => m.confirmed).reduce((s, m) => s + m.amount, 0) ?? 0
)
const confirmedCount = computed(() =>
  session.value?.members.filter(m => m.confirmed).length ?? 0
)
const progressPercent = computed(() => {
  if (!totalAmount.value) return 0
  return Math.round((paidAmount.value / totalAmount.value) * 100)
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

function initials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

function formatMoney(n) {
  return Math.round(n || 0).toLocaleString('vi-VN') + 'đ'
}

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  load()
  timer = setInterval(load, 10000)
})
onUnmounted(() => clearInterval(timer))
</script>
