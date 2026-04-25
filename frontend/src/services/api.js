import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export const createSession = (data) => http.post('/sessions', data).then(r => r.data)
export const getSession = (id) => http.get(`/sessions/${id}`).then(r => r.data)
export const confirmPayment = (id, memberName) =>
  http.post(`/sessions/${id}/confirm`, { member_name: memberName }).then(r => r.data)
