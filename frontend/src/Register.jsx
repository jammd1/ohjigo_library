import React, { useState } from 'react';
import { registerUser } from './api'; 
import { useNavigate, Link } from 'react-router-dom'; 
import './RegisterPage.css';

function Register() {
  const [sid, setSid] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  
  const navigate = useNavigate(); // 3. 페이지 이동 함수 초기화

  const handleSubmit = async (e) => {
    e.preventDefault(); 

    if (password !== passwordConfirm) {
      alert('비밀번호가 일치하지 않습니다.');
      return; 
    }

    const userData = { sid, name, email, password };

    // 4. (핵심) API 호출 로직
    try {
      // 5. api.js의 registerUser 함수 호출
      const response = await registerUser(userData);
      
      console.log('회원가입 성공:', response.data);
      alert(`${response.data.name}님, 회원가입이 완료되었습니다. 로그인해주세요.`);
      
      // 6. 회원가입 성공 시 로그인 페이지로 이동
      navigate('/login'); 

    } catch (error) {
      // 7. API 에러 처리 (예: 학번/이메일 중복)
      console.error('회원가입 실패:', error.response ? error.response.data : error.message);
      
      if (error.response && error.response.status === 400) {
        // DRF가 보낸 유효성 검사 에러 (JSON 형태)
        const errorData = error.response.data;
        let errorMessage = '회원가입에 실패했습니다.\n';
        
        // 백엔드에서 온 에러 메시지를 예쁘게 표시
        if (errorData.sid) errorMessage += `학번: ${errorData.sid.join(' ')}\n`;
        if (errorData.email) errorMessage += `이메일: ${errorData.email.join(' ')}\n`;
        
        alert(errorMessage);
      } else {
        alert('회원가입 중 오류가 발생했습니다. (서버 오류 등)');
      }
    }
  };

  return (
    <main className="main-content register-page">
      <br /><br /><h1>회원가입</h1>
      
      <div className="info-section">
        <h2>회원 정보 입력</h2>
        
        {/* 폼 JSX는 이전과 동일 */}
        <form onSubmit={handleSubmit} className="register-form">
          {/* 학번 */}
          <div className="form-group">
            <label htmlFor="sid-input">학번</label>
            <input 
              type="text" id="sid-input" value={sid}
              onChange={(e) => setSid(e.target.value)} required autoFocus
            />
          </div>
          {/* 이름 */}
          <div className="form-group">
            <label htmlFor="name-input">이름 (실명 또는 닉네임)</label>
            <input 
              type="text" id="name-input" value={name}
              onChange={(e) => setName(e.target.value)} required
            />
          </div>
          {/* 이메일 */}
          <div className="form-group">
            <label htmlFor="email-input">이메일</label>
            <input 
              type="email" id="email-input" value={email}
              onChange={(e) => setEmail(e.target.value)} required
            />
          </div>
          {/* 비밀번호 */}
          <div className="form-group">
            <label htmlFor="password-input">비밀번호</label>
            <input 
              type="password" id="password-input" value={password}
              onChange={(e) => setPassword(e.target.value)} required
            />
          </div>
          {/* 비밀번호 확인 */}
          <div className="form-group">
            <label htmlFor="password-confirm-input">비밀번호 확인</label>
            <input 
              type="password" id="password-confirm-input" value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)} required
            />
          </div>
          <button type="submit" className="register-submit-button">
            가입하기
          </button>
        </form>
        
        <p style={{ marginTop: '20px', textAlign: 'center' }}>
        이미 계정이 있으신가요? <Link to="/login">로그인</Link>
        </p>
      </div>
    </main>
  );
}

export default Register;