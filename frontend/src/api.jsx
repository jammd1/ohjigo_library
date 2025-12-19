// src/api.jsx

// 1. axios 직접 임포트 대신, 우리가 만든 http 설정(인스턴스)을 가져옵니다.
import api from './api/http'; 

/**
 * 회원가입 API
 * (baseURL + '/members/' 로 요청)
 */
export const registerUser = async (userData) => {
  // api 인스턴스에 이미 baseURL이 설정되어 있으므로 경로만 적습니다.
  const response = await api.post('/members/', userData);
  return response.data;
};

/**
 * 로그인 (JWT 토큰 발급) API
 */
export const loginUser = async (sid, password) => {
  try {
    // baseURL + '/token/' 로 요청
    const response = await api.post('/api/token/', {
      sid: sid, 
      password: password,
    });
    
    // 토큰 저장 로직
    const { access, refresh, name, sid: userSid } = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('userName', name); // 이름 저장
    localStorage.setItem('userSid', userSid); // 학번 저장

    // 앞으로 보내는 모든 요청 헤더에 토큰을 자동으로 붙입니다.
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;

    return response.data;

  } catch (error) {
    // 실패 시 기존 토큰 삭제
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    delete api.defaults.headers.common['Authorization'];
    throw error;
  }
};

/**
 * 로그아웃
 */
export const logoutUser = () => {
  localStorage.clear(); // 로컬 스토리지 싹 비우기
  delete api.defaults.headers.common['Authorization'];
};

// 다른 곳에서 api 인스턴스를 직접 쓸 수 있게 내보냅니다.
export default api;