// src/api.jsx
import api from './api/http'; 

export const registerUser = async (userData) => {
  const response = await api.post('/api/members/', userData);
  return response.data;
};

export const loginUser = async (sid, password) => {
  try {
    // String(sid)를 통해 서버가 기대하는 문자열 포맷으로 전달
    const response = await api.post('/api/token/', {
      username: String(sid), 
      password: String(password),
    });
    
    const { access, refresh, name, sid: userSid, role } = response.data;
    
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('userName', name);
    localStorage.setItem('userSid', userSid);
    localStorage.setItem('userRole', role); // 역할 정보 추가 저장

    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    return response.data;

  } catch (error) {
    localStorage.clear();
    delete api.defaults.headers.common['Authorization'];
    throw error;
  }
};

export const logoutUser = () => {
  localStorage.clear();
  delete api.defaults.headers.common['Authorization'];
};

export default api;