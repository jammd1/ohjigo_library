// src/App.jsx (수정 완료)

// 👈 1. useNavigate 훅을 react-router-dom에서 임포트합니다.
import { Routes, Route, Link, Outlet, useNavigate } from 'react-router-dom';
import Info from './Info';
import About from './About';
import Login from './Login'; 
import Register from './Register'; 
import simbol from '../img/simbol.png';
import mainBanner from '../img/main_banner.jpg';
import './App.css';
import { useAuth } from './AuthContext'; // (이건 이미 있음)

// ... (HomePage 컴포넌트는 수정 없음) ...
function HomePage() {
  return (
    <>
      {/* ... (HomePage JSX 내용) ... */}
      <div className="hero-section">
        <img src={mainBanner} alt="메인 배너 이미지" className="main-banner-image" />
        <section className="search-section" aria-label="Search Section">
          <form className="search-container" role="search">
            <label htmlFor="search-input" className="visually-hidden">통합검색</label>
            <input type="search" id="search-input" className="rectangle-3" placeholder="홈페이지 제작 중" />
            <button className="rectangle-4" type="submit" aria-label="검색">
              <span className="visually-hidden">검색</span>
            </button>
          </form>
        </section>
      </div>
      <main className="main-content">
        <section className="content-sections">
          <article className="schedule-section" aria-labelledby="schedule-heading">
            <h2 id="schedule-heading">도서관 일정</h2>
            <div className="line"></div>
            <ul id="schedule-list" className="info-list">
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
            </ul>
          </article>
          <article className="notice-section" aria-labelledby="notice-heading">
            <h2 id="notice-heading">공지</h2>
            <div className="img"></div>
            <ul id="notice-list" className="info-list">
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
              <li><a href="#">- 도서관 홈페이지 제작 중입니다</a></li>
            </ul>
          </article>
        </section>
      </main>
    </>
  );
}

function Layout() {
  const { isLoggedIn, user, logout } = useAuth();
  const navigate = useNavigate();

  // 👈 1. (e) => 를 추가 (event 객체를 받음)
  const handleLogout = (e) => {
    // 👈 2. (핵심) <a> 태그의 기본 href 동작을 막습니다.
    e.preventDefault(); 
    
    logout();      // 1. Context의 logout 함수
    navigate('/'); // 2. 메인 페이지('/')로 이동
  };

  return (
    <div className="desktop">
      <header className="header">
        <div className="header-top">
          <nav className="utility-nav" aria-label="Utility Navigation">
            <a href="https://deutsch.hufs.ac.kr/sites/deutsch/index.do">독일어과 home</a>
            <a href="https://www.hufs.ac.kr/sites/hufs/index.do">HUFS home</a>
            
            {isLoggedIn ? (
              <>
                <Link to="/mypage" style={{marginRight: '5px'}}>{user?.name}님</Link> / 
                
                {/* 👈 4. onClick 이벤트를 'logout' 대신 'handleLogout'으로 변경합니다. */}
                <a href="#!" onClick={handleLogout} style={{marginLeft: '5px', cursor: 'pointer'}}>로그아웃</a>
              </>
            ) : (
              <>
                <Link to="/login">로그인</Link> / <Link to="/register">회원가입</Link>
              </>
            )}
          </nav>
        </div>
        {/* ... (header-main, footer 등 나머지는 동일) ... */}
        <div className="header-main">
          <Link to="/" className="site-title">
            <img src={simbol} alt="오스트리아 도서관 로고" className="logo-image" />
            <p className="austrian-library">
              Austrian Library<br />Bibliothek der Österreich<br />한국외국어대학교 <strong>오스트리아 도서관</strong>
            </p>
          </Link>
          <nav className="main-nav" aria-label="Main Navigation">
            <a href="#">자료 검색</a>
            <a href="#">공지</a>
            <a href="#">내 서재</a>
            <Link to="/info">도서관 안내</Link>
            <Link to="/about">도서관 소개</Link>
          </nav>
        </div>
      </header>
      <Outlet /> 
      <footer className="footer">
        <div className="footer-content">
          <address className="element">
            <strong>주소</strong><br />
            02450 서울특별시 동대문구 이문로 107 한국외국어대학교 서울캠퍼스 본관 301호<br />
            서양어대학 독일어과 오스트리아도서관<br /><br />
            <strong>TEL.</strong> 02-2173-2283<br />
            <strong>Email.</strong> deutsch@hufs.ac.kr
          </address>
          <div className="element operating-hours">
            <strong>운영 시간</strong><br />
            학기 중 09:00~17:00<br />
            방학 중 10:00~15:00<br />
            점심시간 12:00~13:00
          </div>
          <div className="element-developer">
            <strong>개발자 정보</strong><br />독일어('23) woals6318@hufs.ac.kr<br />독일어('24) jsjang0104@naver.com<br />Language&AI융합('24) ericyang@hufs.ac.kr
          </div>
        </div>
      </footer>
    </div>
  );
}

// ... (App 컴포넌트 라우터 설정은 수정 없음) ...
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="info" element={<Info />} />
        <Route path="about" element={<About />} />
        <Route path="login" element={<Login />} /> 
        <Route path="register" element={<Register />} />
      </Route>
    </Routes>
  );
}

export default App;