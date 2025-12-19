import axios from 'axios';

const http = axios.create({
  // 환경 변수 쓰지 말고, 실제 Render 백엔드 주소를 직접 따옴표 안에 넣으세요.
  baseURL: 'https://ohjigo-library.onrender.com/api/', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;