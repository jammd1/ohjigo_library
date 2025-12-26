import React, { createContext, useContext, useState, useEffect } from 'react';
import api from './api/http';


const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    const userName = localStorage.getItem('userName');
    const userSid = localStorage.getItem('userSid');

    if (accessToken && userName && userSid) {
      setIsLoggedIn(true);
      setUser({ name: userName, sid: userSid });
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    }
  }, []);


  const login = (data) => {
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    localStorage.setItem('userName', data.name);
    localStorage.setItem('userSid', data.sid);

    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

    setIsLoggedIn(true);
    setUser({ name: data.name, sid: data.sid });
  };

  const logout = () => {
    localStorage.clear(); 
    delete api.defaults.headers.common['Authorization']; 
    setIsLoggedIn(false);
    setUser(null);
  };

  const value = {
    isLoggedIn,
    user,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  return useContext(AuthContext);
};