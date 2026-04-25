<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-else-if="!session" class="empty">Session not found</div>
  <div v-else-if="done" class="confirm-done">
    <div class="done-icon">✓</div>
    <h2>Confirmed!</h2>
    <p>Payment recorded for: <strong>{{ confirmedNames.join(', ') }}</strong></p>
  </div>
  <div v-else class="confirm-page">
    <h2>{{ session.name }}</h2>
    <p class="hint">Select who you're paying for</p>

    <div class="member-list">
      <button
        v-for="m in session.members"
        :key="m.name"
        class="member-btn"
        :class="{ selected: selectedNames.includes(m.name), confirmed: m.confirmed }"
        :disabled="m.confirmed"
        @click="onSelectMember(m.name)"
      >
        <span class="member-check" v-if="selectedNames.includes(m.name)">✓</span>
        <span>{{ m.name }}</span>
        <span class="member-amount">{{ formatMoney(m.amount) }}</span>
        <span v-if="m.confirmed" class="member-tag">✓ Paid</span>
      </button>
    </div>

    <button
      class="btn-submit"
      :disabled="selectedNames.length === 0 || confirming"
      @click="showFinalConfirm = true"
    >
      {{ confirming ? 'Confirming...' : `I have paid (${selectedNames.length})` }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>

  <!-- Popup: confirm adding extra person -->
  <div v-if="pendingName" class="popup-overlay" @click.self="pendingName = ''">
    <div class="popup">
      <p>You're paying for <strong>{{ selectedNames.join(', ') }}</strong>. Also pay for <strong>{{ pendingName }}</strong>?</p>
      <div class="popup-actions">
        <button class="btn-cancel" @click="pendingName = ''">Cancel</button>
        <button class="btn-confirm-pop" @click="confirmAddPending">Yes, add</button>
      </div>
    </div>
  </div>

  <!-- Popup: final confirm -->
  <div v-if="showFinalConfirm" class="popup-overlay" @click.self="showFinalConfirm = false">
    <div class="popup">
      <p>Confirm payment for:</p>
      <ul class="confirm-list">
        <li v-for="n in selectedNames" :key="n">{{ n }} — {{ formatMoney(amountFor(n)) }}</li>
      </ul>
      <div class="popup-actions">
        <button class="btn-cancel" @click="showFinalConfirm = false">Cancel</button>
        <button class="btn-confirm-pop" @click="onConfirm">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSession, confirmPayment } from '../services/api'

const route = useRoute()
const session = ref(null)
const loading = ref(true)
const selectedNames = ref([])
const confirmedNames = ref([])
const pendingName = ref('')
const showFinalConfirm = ref(false)
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

function onSelectMember(name) {
  if (selectedNames.value.includes(name)) {
    selectedNames.value = selectedNames.value.filter(n => n !== name)
    return
  }
  if (selectedNames.value.length === 0) {
    selectedNames.value.push(name)
  } else {
    pendingName.value = name
  }
}

function confirmAddPending() {
  selectedNames.value.push(pendingName.value)
  pendingName.value = ''
}

function amountFor(name) {
  return session.value?.members.find(m => m.name === name)?.amount ?? 0
}

async function onConfirm() {
  showFinalConfirm.value = false
  confirming.value = true
  error.value = ''
  try {
    for (const name of selectedNames.value) {
      await confirmPayment(route.params.id, name)
    }
    confirmedNames.value = [...selectedNames.value]
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
