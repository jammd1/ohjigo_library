import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // base: '/ohjigo_library/',  <-- ✅ 이 줄을 삭제하거나 주석 처리하세요!

  server: {
    proxy: {
      '/api': {
        target: 'https://ohjigo-library.onrender.com',
        changeOrigin: true,
      }
    }
  }
})