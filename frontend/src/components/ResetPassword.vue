<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🔐</div>
      <div class="auth-header">
        <h2>Set new password</h2>
        <p class="auth-subtitle">Choose a strong password for your account</p>
      </div>

      <div v-if="done" class="sent-msg">
        ✓ Password reset! <router-link to="/login">Sign in</router-link>
      </div>

      <form v-else @submit.prevent="onSubmit" class="auth-form">
        <div class="field">
          <label>New password</label>
          <input v-model="password" type="password" placeholder="••••••••" autocomplete="new-password" required />
          <span class="field-hint">Min 8 chars, uppercase, lowercase, number</span>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="btn-submit" type="submit" :disabled="loading">
          {{ loading ? 'Resetting...' : 'Reset password' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const password = ref('')
const loading = ref(false)
const error = ref('')
const done = ref(false)

async function onSubmit() {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/api/auth/reset-password', {
      token: route.query.token,
      new_password: password.value,
    })
    done.value = true
  } catch (err) {
    error.value = err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || 'Invalid or expired link'
  } finally {
    loading.value = false
  }
}
</script>
