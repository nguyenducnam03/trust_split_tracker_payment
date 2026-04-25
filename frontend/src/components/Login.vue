<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">💸</div>
      <div class="auth-header">
        <h2>{{ isRegister ? 'Create Account' : 'Welcome back' }}</h2>
        <p class="auth-subtitle">{{ isRegister ? 'Start tracking your group payments' : 'Sign in to manage your sessions' }}</p>
      </div>

      <form @submit.prevent="onSubmit" class="auth-form">
        <div class="field" v-if="isRegister">
          <label>Name</label>
          <input v-model="name" type="text" placeholder="Your name" autocomplete="name" required />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="you@example.com" autocomplete="email" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="••••••••" :autocomplete="isRegister ? 'new-password' : 'current-password'" required />
          <span v-if="isRegister" class="field-hint">Min 8 chars, uppercase, lowercase, number</span>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button class="btn-submit" type="submit" :disabled="loading">
          {{ loading ? 'Please wait...' : (isRegister ? 'Create Account' : 'Sign In') }}
        </button>
      </form>

      <p v-if="!isRegister" class="auth-switch">
        <router-link to="/forgot-password">Forgot password?</router-link>
      </p>
      <p class="auth-switch">
        {{ isRegister ? 'Already have an account?' : "Don't have an account?" }}
        <a href="#" @click.prevent="isRegister = !isRegister; error = ''">
          {{ isRegister ? 'Sign In' : 'Create one' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../services/auth'

const router = useRouter()
const isRegister = ref(false)
const email = ref('')
const password = ref('')
const name = ref('')
const loading = ref(false)
const error = ref('')

async function onSubmit() {
  loading.value = true
  error.value = ''
  try {
    if (isRegister.value) {
      await register(email.value, password.value, name.value)
    } else {
      await login(email.value, password.value)
    }
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
