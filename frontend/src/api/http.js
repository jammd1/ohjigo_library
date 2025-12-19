import axios from 'axios';

const http = axios.create({
  // 환경 변수 대신 실제 Render 백엔드 주소를 직접 넣습니다.
  // 주소 끝에 /api를 꼭 확인하세요!
  baseURL: 'https://ohjigo-library.onrender.com/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;