//======================================================================
//======================================================================
// 로그인 (완료)
//======================================================================
//======================================================================
import React, { useState } from 'react'; 
import { useAuth } from './AuthContext';
import { loginUser } from './api'; 
import { useNavigate, Link } from 'react-router-dom'; 
import './LoginPage.css';

function Login() {
  const [sid, setSid] = useState('');
  const [password, setPassword] = useState('');
  
  const navigate = useNavigate();
  const { login } = useAuth(); // 👈 2. AuthContext에서 login 함수 가져오기

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const responseData = await loginUser(sid, password);
      
      // 3. (핵심) Context의 login 함수 호출
      //    이 함수가 알아서 localStorage 저장 + 전역 상태 변경
      login(responseData); 
      
      console.log('로그인 성공:', responseData);
      alert('로그인에 성공했습니다!');
      
      // 4. 메인 페이지로 이동
      navigate('/');
      
    } catch (error) {
      // (이하 에러 처리 로직은 동일)
      console.error('로그인 실패:', error.response ? error.response.data : error.message);
      if (error.response && (error.response.status === 401 || error.response.status === 400)) {
        alert('학번 또는 비밀번호가 일치하지 않습니다.');
      } else {
        alert('로그인 중 오류가 발생했습니다.');
      }
      setPassword('');
    }
  };

  return (
    <main className="main-content login-page">
      <br /><br /><h1>로그인</h1>
      
      <div className="info-section">
        <h2>회원 로그인</h2>

        {/* 폼 JSX는 이전과 동일 */}
        <form onSubmit={handleSubmit} className="login-form">
          {/* 학번 */}
          <div className="form-group">
            <label htmlFor="sid-input">학번</label>
            <input 
              type="text" id="sid-input" value={sid}
              onChange={(e) => setSid(e.target.value)} required autoFocus
            />
          </div>
          {/* 비밀번호(전화번호) */}
          <div className="form-group">
            <label htmlFor="password-input">비밀번호</label>
            <input 
              type="password" id="password-input" value={password}
              onChange={(e) => setPassword(e.target.value)} required
            />
          </div>
          <button type="submit" className="login-submit-button">
            로그인
          </button>
        </form>
        
        <p style={{ marginTop: '20px', textAlign: 'center' }}>
        계정이 없으신가요? <Link to="/register">회원가입</Link>
        </p>
      </div>
    </main>
  );
}

export default Login;