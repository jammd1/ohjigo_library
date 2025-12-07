import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import './global.css';
import App from './App.jsx';
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