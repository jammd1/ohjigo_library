// 회원가입, 로그인, 로그아웃 API

import axios from 'axios';

// 1. (핵심) baseURL이 '.../api'로 끝나야 합니다.
const API_URL = 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
});

// (토큰 자동 설정 로직)
const accessToken = localStorage.getItem('accessToken');
if (accessToken) {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}

/**
 * 회원가입 API
 * (baseURL + '/members/' = /api/members/ 로 요청)
 */
export const registerUser = (userData) => {
  return apiClient.post('/members/', userData);
};

/**
 * 로그인 (JWT 토큰 발급) API
 */
export const loginUser = async (sid, password) => {
  try {
    // (baseURL + '/token/' = /api/token/ 로 요청)
    const response = await apiClient.post('/token/', {
      
      // 2. (핵심) 'username:'이 아니라 'sid:' 입니다.
      sid: sid, 
      password: password,
    });
    
    // (토큰 저장 로직)
    const { access, refresh } = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`;

    return response.data;

  } catch (error) {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    delete apiClient.defaults.headers.common['Authorization'];
    throw error;
  }
};

/**
 * 로그아웃
 */
export const logoutUser = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  delete apiClient.defaults.headers.common['Authorization'];
};

export default apiClient;