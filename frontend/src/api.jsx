import api from './api/http'; 

export const registerUser = async (userData) => {
  const response = await api.post('/api/members/', userData);
  return response.data;
};

export const loginUser = async (sid, password) => {
  try {
    const response = await api.post('/api/token/', {
      username: String(sid), 
      password: String(password),
    });
    
    const { access, refresh, name, sid: userSid, role } = response.data;
    
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('userName', name);
    localStorage.setItem('userSid', userSid);
    localStorage.setItem('userRole', role); 

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