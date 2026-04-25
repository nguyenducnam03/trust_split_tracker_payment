<template>
  <div>
    <Navbar v-if="showNavbar" />
    <div class="container">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { authState } from './services/auth'

const route = useRoute()
const showNavbar = computed(() => authState.value && route.path !== '/login')
</script>
