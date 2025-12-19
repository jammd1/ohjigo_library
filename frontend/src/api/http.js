import axios from 'axios';

const http = axios.create({
  // 환경 변수에서 주소를 가져오고, 없으면 기본값 사용
  baseURL: import.meta.env.VITE_API_URL, 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;