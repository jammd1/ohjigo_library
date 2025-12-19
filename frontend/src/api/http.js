// src/api/http.js
import axios from 'axios';

const http = axios.create({
  // 끝에 /api를 쓰지 마세요. 도메인까지만 쓰세요.
  baseURL: 'https://ohjigo-library.onrender.com', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;