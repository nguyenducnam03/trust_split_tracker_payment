<template>
  <nav class="navbar">
    <router-link to="/" class="nav-brand">💸 SplitTrack</router-link>
    <div class="nav-right" v-if="user">
      <span class="nav-user">{{ user.name }}</span>
      <button class="btn-logout" @click="onLogout">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { getUser, logout } from '../services/auth'

const user = computed(() => getUser())

function onLogout() {
  logout()
}
</script>
