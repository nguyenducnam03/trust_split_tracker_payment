import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [vue()],
    server: {
      allowedHosts: ['localhost', '.ngrok-free.app', '.ngrok-free.dev'],
      proxy: {
        '/api': env.VITE_API_URL || 'http://localhost:7776',
      },
    },
  }
})
