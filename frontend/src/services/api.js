import axios from 'axios'
import { getAccessToken, refreshAccessToken, logout } from './auth'

const http = axios.create({ baseURL: '/api' })

http.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        const newToken = await refreshAccessToken()
        original.headers.Authorization = `Bearer ${newToken}`
        return http(original)
      } catch {
        logout()
      }
    }
    return Promise.reject(err)
  }
)

export const getSessions = () => http.get('/sessions').then(r => r.data)
export const createSession = (data) => http.post('/sessions', data).then(r => r.data)
export const getSession = (id) => http.get(`/sessions/${id}`).then(r => r.data)
export const confirmPayment = (id, memberName) =>
  http.post(`/sessions/${id}/confirm`, { member_name: memberName }).then(r => r.data)
