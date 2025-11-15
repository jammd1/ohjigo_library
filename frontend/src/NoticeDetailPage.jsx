import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

function NoticeDetailPage() {
  // 1. URL 파라미터에서 noticeId 값을 가져옵니다. (예: /notice/3 -> noticeId = '3')
  const { noticeId } = useParams();
  
  // 2. '단일' 공지사항, 로딩, 에러 상태
  const [notice, setNotice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 3. noticeId가 바뀔 때마다 API를 호출합니다.
  useEffect(() => {
    const fetchNoticeDetail = async () => {
      try {
        setNotice(null);
        setError(null);
        setLoading(true);

        // 4. (중요!) '목록'이 아닌 '상세' API를 호출합니다.
        // Django REST Framework는 보통 /api/books/notices/<id>/ 형태를 사용합니다.
        const response = await axios.get(`/api/books/notices/${noticeId}/`);
        
        setNotice(response.data);
      } catch (e) {
        setError(e);
      }
      setLoading(false);
    };

    fetchNoticeDetail();
  }, [noticeId]); // noticeId가 변경될 때마다 이 effect를 다시 실행합니다.

  // --- 로딩 및 에러 UI ---
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

  // --- 성공 시 상세 페이지 UI ---
  // notice가 null이거나 찾을 수 없을 때의 처리
  if (!notice) {
    return (
      <main className="main-content about-page">
        <br /><br /><h1>공지</h1>
        <div className="about-section">
          <p>해당 공지사항을 찾을 수 없습니다.</p>
          <Link to="/board">목록으로 돌아가기</Link>
        </div>
      </main>
    );
  }

  // notice 객체를 성공적으로 받아왔을 때
  return (
    <main className="main-content about-page">
      <br /><br />
      
      {/* 1. 제목 (h1) */}
      <h1>{notice.title}</h1>

      <div className="about-section">
        
        {/* 2. 메타데이터 (작성자, 작성일, 조회수) */}
        <div style={{ 
          fontSize: '0.9rem', 
          color: '#666',
          paddingBottom: '16px', 
          marginBottom: '24px', 
          borderBottom: '1px solid #eee' 
        }}>
          <span style={{ marginRight: '12px' }}>
            {/* 'manager'가 ID로 나올 경우, 이름으로 표시는 백엔드 수정이 필요합니다. */}
            작성자: {notice.manager || 'N/A'}
          </span>
          <span style={{ marginRight: '12px' }}>
            작성일: {new Date(notice.post_date).toLocaleDateString()}
          </span>
          <span>
            조회수: {notice.view_count}
          </span>
        </div>
        
        {/* 3. 본문 내용 (content) */}
        <div 
          className="notice-content"
          style={{ 
            minHeight: '200px', // 최소 높이
            lineHeight: '1.6', // 줄 간격
            fontSize: '1rem',
            // [!] Django의 TextField는 '\n' (줄바꿈)을 그대로 저장합니다.
            // 'whiteSpace: pre-wrap'은 이 \n을 HTML <br> 태그처럼 인식하게 해줍니다.
            whiteSpace: 'pre-wrap' 
          }}
        >
          {notice.content}
        </div>

        {/* 4. 목록으로 돌아가기 버튼 */}
        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <Link 
            to="/board" 
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#f0f0f0', 
              color: '#333',
              textDecoration: 'none',
              borderRadius: '5px'
            }}
          >
            목록으로
          </Link>
        </div>

      </div>
    </main>
  );
}

export default NoticeDetailPage;