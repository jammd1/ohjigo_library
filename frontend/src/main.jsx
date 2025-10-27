// src/index.jsx (수정 완료)

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import './global.css';
import App from './App.jsx';

// 👈 1. AuthProvider를 임포트합니다. (경로가 맞는지 확인)
import { AuthProvider } from './AuthContext'; 

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* 👈 2. AuthProvider가 HashRouter를 감싸도록 수정 */}
    <AuthProvider>
      <HashRouter>
        <App />
      </HashRouter>
    </AuthProvider>
  </StrictMode>,
);