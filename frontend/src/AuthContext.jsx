// src/AuthContext.js

import React, { createContext, useContext, useState, useEffect } from 'react';
import api from './api/http';

// 1. Context 생성
const AuthContext = createContext();

// 2. Context Provider (앱을 감쌀 컴포넌트)
export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // 3. (핵심) 앱 첫 로드 시 localStorage에서 토큰을 확인
  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    const userName = localStorage.getItem('userName');
    const userSid = localStorage.getItem('userSid');

    if (accessToken && userName && userSid) {
      // 토큰이 있으면 로그인 상태로 설정
      setIsLoggedIn(true);
      setUser({ name: userName, sid: userSid });
      // (중요) api.js의 axios 헤더에도 토큰 다시 설정
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    }
  }, []);

  // 4. 로그인 함수 (Login.js가 호출할 함수)
  const login = (data) => {
    // 백엔드에서 받은 토큰과 사용자 정보를 localStorage에 저장
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    localStorage.setItem('userName', data.name);
    localStorage.setItem('userSid', data.sid);

    // (중요) api.js의 axios 헤더에 토큰 바로 설정
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

    // 앱의 전역 상태를 '로그인 됨'으로 변경
    setIsLoggedIn(true);
    setUser({ name: data.name, sid: data.sid });
  };

  // 5. 로그아웃 함수 (Navbar가 호출할 함수)
  const logout = () => {
    localStorage.clear(); // localStorage 싹 비우기
    delete api.defaults.headers.common['Authorization']; // axios 헤더에서 토큰 제거
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

// 6. 커스텀 Hook (다른 컴포넌트에서 쉽게 쓰기 위함)
export const useAuth = () => {
  return useContext(AuthContext);
};