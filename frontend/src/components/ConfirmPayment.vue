<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-else-if="!session" class="empty">Session not found</div>
  <div v-else-if="done" class="confirm-done">
    <div class="done-icon">✓</div>
    <h2>Confirmed!</h2>
    <p>Thanks {{ selectedName }}, your payment has been recorded.</p>
  </div>
  <div v-else class="confirm-page">
    <h2>{{ session.name }}</h2>
    <p class="hint">Select your name to confirm payment</p>

    <div class="member-list">
      <button
        v-for="m in session.members"
        :key="m.name"
        class="member-btn"
        :class="{ selected: selectedName === m.name, confirmed: m.confirmed }"
        :disabled="m.confirmed"
        @click="selectedName = m.name"
      >
        <span>{{ m.name }}</span>
        <span class="member-amount">{{ formatMoney(m.amount) }}</span>
        <span v-if="m.confirmed" class="member-tag">✓ Paid</span>
      </button>
    </div>

    <button class="btn-submit" :disabled="!selectedName || confirming" @click="onConfirm">
      {{ confirming ? 'Confirming...' : 'I have paid' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSession, confirmPayment } from '../services/api'

const route = useRoute()
const session = ref(null)
const loading = ref(true)
const selectedName = ref('')
const confirming = ref(false)
const done = ref(false)
const error = ref('')

async function load() {
  try {
    session.value = await getSession(route.params.id)
  } catch {
    session.value = null
  } finally {
    loading.value = false
  }
}

async function onConfirm() {
  confirming.value = true
  error.value = ''
  try {
    await confirmPayment(route.params.id, selectedName.value)
    done.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong'
  } finally {
    confirming.value = false
  }
}

function formatMoney(n) {
  return Math.round(n || 0).toLocaleString('vi-VN') + 'đ'
}

onMounted(load)
</script>
