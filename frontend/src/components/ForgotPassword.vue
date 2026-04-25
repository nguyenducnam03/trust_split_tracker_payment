<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🔑</div>
      <div class="auth-header">
        <h2>Forgot password?</h2>
        <p class="auth-subtitle">Enter your email and we'll send you a reset link</p>
      </div>

      <div v-if="sent" class="sent-msg">
        ✓ Check your email for a reset link
      </div>

      <form v-else @submit.prevent="onSubmit" class="auth-form">
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="you@example.com" autocomplete="email" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="btn-submit" type="submit" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send reset link' }}
        </button>
      </form>

      <p class="auth-switch">
        <router-link to="/login">← Back to Sign In</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const loading = ref(false)
const error = ref('')
const sent = ref(false)

async function onSubmit() {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/api/auth/forgot-password', { email: email.value })
    sent.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
