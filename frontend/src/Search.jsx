import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom'; // ★ URL 파라미터 사용을 위해 추가
import http from './api/http';
import './App.css';

function Search() {
  // 1. URL 파라미터 훅 (메인 페이지에서 넘어온 ?search=... 값을 읽기 위함)
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQuery = searchParams.get('search') || '';

  // 2. 상태 관리
  const [keyword, setKeyword] = useState(initialQuery); // 초기값을 URL에서 가져옴
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  // ★ 필터 상태 추가
  const [selectedLang, setSelectedLang] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');

  // 3. 맵핑 객체 (백엔드 데이터와 화면 표시용)
  // 주의: 백엔드가 소문자('available')로 보내는지 대문자('AVAILABLE')로 보내는지 확인 후 키값을 맞춰야 합니다.
  // 여기서는 안전하게 둘 다 처리하도록 작성했습니다.
  const STATUS_MAP = {
    'AVAILABLE': '대출 가능', 'available': '대출 가능',
    'ON_LOAN': '대출 중',     'loaned': '대출 중',
    'LOST': '분실',          'lost': '분실'
  };

  const LANG_MAP = {
    'KR': '한국어', 'Korean': '한국어',
    'DE': '독일어', 'Deutsch': '독일어',
    'EN': '영어',   'English': '영어',
    'ETC': '기타'
  };

  // 4. 통합 검색 함수 (검색어 + 필터)
  const fetchBooks = async (searchKeyword) => {
    try {
      setLoading(true);
      
      // 백엔드로 보낼 파라미터 구성
      const params = {
        search: searchKeyword,         // 검색어
        language: selectedLang,        // 언어 필터
        category: selectedCategory,    // 분야 필터
        status: selectedStatus         // 상태 필터
      };

      // 값이 없는 필터는 전송하지 않음 (깔끔한 URL 요청을 위해)
      const cleanParams = Object.fromEntries(
        Object.entries(params).filter(([_, v]) => v !== '')
      );

      const response = await http.get('/api/books/', { params: cleanParams });
      
      console.log("검색 성공:", response.data);
      setBooks(response.data);
      setSearched(true); // 검색 시도함 표시

    } catch (error) {
      console.error("검색 실패:", error);
    } finally {
      setLoading(false);
    }
  };

  // 5. [효과 1] 페이지 접속 시 URL에 검색어가 있으면 자동 검색
  useEffect(() => {
    if (initialQuery) {
      fetchBooks(initialQuery);
    }
  }, []); 

  // 6. [효과 2] 필터가 변경되면 즉시 재검색
  useEffect(() => {
    // 검색어가 있거나 필터 중 하나라도 설정되어 있으면 검색 실행
    if (searched || keyword || selectedLang || selectedCategory || selectedStatus) {
       fetchBooks(keyword);
    }
  }, [selectedLang, selectedCategory, selectedStatus]);


  // 7. 검색 버튼 클릭 핸들러
  const handleSearch = (e) => {
    e.preventDefault();
    // URL 주소창도 업데이트 (새로고침 해도 유지되도록)
    setSearchParams({ search: keyword });
    fetchBooks(keyword);
  };

  return (
    <main className="main-content info-page">
      <br /><br />
      <h1>자료 검색</h1>

      {/* 검색창 섹션 */}
      <div className="info-section search-wrapper">
        <form onSubmit={handleSearch} className="library-search-form" style={{ flexDirection: 'column', gap: '15px' }}>
          
          {/* 상단: 검색어 입력 */}
          <div style={{ display: 'flex', width: '100%', gap: '10px' }}>
            <input 
              type="text" 
              placeholder="도서명, 저자, 청구기호 등을 입력하세요" 
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="search-input-lg"
            />
            <button type="submit" className="search-btn-lg">검색</button>
          </div>

          {/* ★ 하단: 필터 선택 (스타일은 기존 테마에 맞춰 심플하게 적용) */}
          <div className="filter-group" style={{ display: 'flex', gap: '10px', width: '100%' }}>
            {/* 언어 선택 */}
            <select 
              value={selectedLang} 
              onChange={(e) => setSelectedLang(e.target.value)}
              className="search-input-lg" // 기존 인풋 스타일 재활용
              style={{ flex: 1, padding: '10px', height: 'auto' }}
            >
              <option value="">-- 언어 전체 --</option>
              <option value="Deutsch">독일어</option>
              <option value="Korean">한국어</option>
              <option value="English">영어</option>
            </select>

            {/* 분야 선택 */}
            <select 
              value={selectedCategory} 
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="search-input-lg"
              style={{ flex: 1, padding: '10px', height: 'auto' }}
            >
              <option value="">-- 분야 전체 --</option>
              <option value="Literatur">문학</option>
              <option value="Sprachwissenschaft">언어학</option>
              <option value="Geschichte">역사</option>
              <option value="Landeskunde">지역학</option>
              <option value="Sonstiges">기타</option>
            </select>

            {/* 상태 선택 */}
            <select 
              value={selectedStatus} 
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="search-input-lg"
              style={{ flex: 1, padding: '10px', height: 'auto' }}
            >
              <option value="">-- 상태 전체 --</option>
              <option value="available">대출 가능</option>
              <option value="loaned">대출 중</option>
            </select>
          </div>

        </form>
      </div>

      {/* 결과 섹션 */}
      <div className="info-section">
        <h2>검색 결과</h2>
        {loading ? (
          <p className="loading-msg">데이터를 불러오는 중입니다...</p>
        ) : (
          <div className="table-container">
            <table className="library-table">
              <thead>
                <tr>
                  <th width="15%">청구기호</th>
                  <th width="30%">제목</th>
                  <th width="15%">저자</th>
                  <th width="10%">언어</th>
                  <th width="10%">분야</th>
                  <th width="10%">위치</th>
                  <th width="10%">상태</th>
                </tr>
              </thead>
              <tbody>
                {books && books.length > 0 ? (
                  books.map((book) => (
                    <tr key={book.id || book.book_id}> 
                      {/* 백엔드 ID 필드명 확인 필요 (id 혹은 book_id) */}
                      <td>{book.call_number}</td>
                      <td className="text-left">{book.title}</td>
                      <td>{book.author || '-'}</td>
                      
                      {/* 맵핑된 값이 있으면 쓰고, 없으면 DB값 그대로 출력 */}
                      <td>{LANG_MAP[book.language] || book.language}</td>
                      <td>{book.category}</td>
                      <td>{book.location || '-'}</td>
                      
                      <td>
                        {/* 상태 뱃지 로직: available이거나 AVAILABLE이면 초록색 */}
                        <span className={`status-badge ${
                          (book.status === 'AVAILABLE' || book.status === 'available') 
                          ? 'available' : 'borrowed'
                        }`}>
                          {STATUS_MAP[book.status] || book.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="7" className="no-result">
                      {searched ? "검색 결과가 없습니다." : "검색어를 입력해 주세요."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}

export default Search;