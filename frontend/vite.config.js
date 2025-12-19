import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  base: '/ohjigo_library/',

  server: {
    proxy: {
      // '/api'로 시작하는 모든 요청을 Django 서버로 보냅니다.
      '/api': {
        target: 'https://ohjigo-library.onrender.com', // Django 서버 주소
        changeOrigin: true, // CORS 오류 방지를 위해 호스트 헤더 변경
      }
    }
  }
  // ------------------------------------
})