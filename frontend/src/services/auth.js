import axios from 'axios'
import { ref } from 'vue'

export const authState = ref(!!localStorage.getItem('tstp_access_token'))

const PREFIX = 'tstp_'
const KEYS = {
  accessToken: `${PREFIX}access_token`,
  refreshToken: `${PREFIX}refresh_token`,
  user: `${PREFIX}user`,
}

const http = axios.create({ baseURL: '/api/auth' })

http.interceptors.request.use((config) => {
  const token = localStorage.getItem(KEYS.accessToken)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export function getAccessToken() {
  return localStorage.getItem(KEYS.accessToken)
}

export function getRefreshToken() {
  return localStorage.getItem(KEYS.refreshToken)
}

export function saveTokens(accessToken, refreshToken) {
  localStorage.setItem(KEYS.accessToken, accessToken)
  localStorage.setItem(KEYS.refreshToken, refreshToken)
  authState.value = true
}

export function saveUser(user) {
  localStorage.setItem(KEYS.user, JSON.stringify(user))
}

export function getUser() {
  const u = localStorage.getItem(KEYS.user)
  return u ? JSON.parse(u) : null
}

export function clearTokens() {
  Object.values(KEYS).forEach(k => localStorage.removeItem(k))
  authState.value = false
}

export function isLoggedIn() {
  return !!getAccessToken()
}

export async function login(email, password) {
  const { data } = await http.post('/login', { email, password })
  saveTokens(data.access_token, data.refresh_token)
  const me = await http.get('/me')
  saveUser(me.data)
  return data
}

export async function register(email, password, name) {
  const { data } = await http.post('/register', { email, password, name })
  saveTokens(data.access_token, data.refresh_token)
  const me = await http.get('/me')
  saveUser(me.data)
  return data
}

export async function refreshAccessToken() {
  const refresh_token = getRefreshToken()
  if (!refresh_token) throw new Error('No refresh token')
  const { data } = await http.post('/refresh', { refresh_token })
  saveTokens(data.access_token, data.refresh_token)
  return data.access_token
}

export function logout() {
  clearTokens()
  window.location.href = '/login'
}
