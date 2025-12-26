import axios from 'axios';

const http = axios.create({
  baseURL: 'https://ohjigo-library.onrender.com', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;