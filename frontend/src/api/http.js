import axios from 'axios';

const http = axios.create({
  // 주소 끝에 /api 를 포함하고, 뒤에 슬래시(/)를 하나 더 붙여주세요.
  baseURL: 'https://ohjigo-library.onrender.com', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;