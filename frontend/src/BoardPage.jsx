//======================================================================
//======================================================================
// 공지사항 (완료)
//======================================================================
//======================================================================
import React, { useState, useEffect } from 'react';
import http from './api/http';
import { Link } from 'react-router-dom';

function BoardPage() {
  const [notices, setNotices] = useState(null); // 초기값을 null로 변경
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // API 호출 함수
    const fetchNotices = async () => {
      try {
        // 1. 요청 시작: 에러/데이터 초기화 및 로딩 시작
        setError(null);
        setNotices(null);
        setLoading(true);

        // 2. API 호출
        const response = await http.get('/api/notices/');
        
        // 3. 요청 성공: 데이터 저장 및 로딩 종료
        setNotices(response.data); 
      } catch (e) {
        // 4. 요청 실패: 에러 저장
        setError(e);
      }
      // 5. 요청 완료 (성공/실패 무관): 로딩 종료
      setLoading(false);
    };

    fetchNotices(); // 함수 실행
  }, []); // [] : 이 컴포넌트가 처음 렌더링될 때 딱 한 번만 실행

  // [수정 5] 로딩 중일 때 표시할 UI
  if (loading) {
    return (
      <main className="main-content about-page">
        <br /><br /><h1>공지</h1>
        <div className="about-section">
          <p>공지사항을 불러오는 중입니다...</p>
        </div>
      </main>
    );
  }

  // [수정 6] 에러 발생 시 표시할 UI
  if (error) {
    return (
      <main className="main-content about-page">
        <br /><br /><h1>공지</h1>
        <div className="about-section">
          <p>오류가 발생했습니다: {error.message}</p>
        </div>
      </main>
    );
  }

  // [수정 7] 데이터가 성공적으로 로드되었을 때 (레이아웃 수정)
  return (
    <main className="main-content about-page">
      <br /><br />
      <h1>공지</h1>

      <div className="about-section">
        
        {/* -- [스타일 수정] --
          - list-style: 'none' : <ul>의 점을 제거합니다.
          - paddingLeft: '0' : <ul>의 기본 왼쪽 여백을 제거합니다.
        */}
        <ul style={{ listStyle: 'none', paddingLeft: '0' }}>
          
          {notices?.length > 0 ? (
            notices.map(notice => (
              
              // -- [스타일 수정] --
              // - 각 <li>에 하단 테두리와 여백을 주어 공지사항을 구분합니다.
              <li 
                key={notice.notice_id} 
                style={{ 
                  paddingBottom: '16px', 
                  marginBottom: '16px', 
                  borderBottom: '1px solid #eee' 
                }}
              > 
                
                {/* 1. 제목 (링크) - 굵게, 첫째 줄 */}
                <div style={{ marginBottom: '8px' }}>
                  <Link 
                    to={`/notice/${notice.notice_id}`}
                    style={{ 
                      fontSize: '1.1rem', 
                      textDecoration: 'none', 
                      color: '#333', 
                      fontWeight: 'bold' 
                    }}
                  >
                    {notice.title} {/* 제목 앞 '-' 제거 */}
                  </Link>
                </div>

                {/* 2. 메타데이터 (작성자, 작성일, 조회수) - 둘째 줄 (왼쪽 정렬) */}
                <div style={{ fontSize: '0.9rem', color: '#666' }}>
                  
                  {/* [!] 'notice.manager'는 관리자 ID(예: 1)를 표시할 수 있습니다.
                        이것이 숫자로 보여도 정상이며,
                        이름(예: "admin")으로 바꾸려면 백엔드 Serializer 수정이 필요합니다.
                  */}
                  <span style={{ marginRight: '12px' }}>
                    작성자: {notice.manager || 'N/A'}
                  </span>

                  <span style={{ marginRight: '12px' }}>
                    작성일: {new Date(notice.post_date).toLocaleDateString()}
                  </span>
                  
                  <span>
                    조회수: {notice.view_count}
                  </span>
                </div>
                
              </li>
            ))
          ) : (
            <li>- 등록된 공지가 없습니다.</li>
          )}
        </ul>
      </div>
    </main>
  );
}

export default BoardPage;