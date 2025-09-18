import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: Number(process.env.FRONTEND_PORT || 5173),
    proxy: {
      '/darkerdb': {
        target: 'https://darkerdb.com',
        rewrite: (path) => path.replace('/darkerdb', '/v1'),
      },
      '/api': {
        target: 'http://172.17.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})


