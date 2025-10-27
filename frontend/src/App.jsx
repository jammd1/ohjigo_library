import { Routes, Route, Link, Outlet } from 'react-router-dom';
import Info from './Info';
import simbol from '../img/simbol.png'; // Import the image
import './App.css';

// Create a simple Home component
function HomePage() {
  return (
    <>
      <h1>Vite + React</h1>
      <p>This is the home page.</p>
    </>
  );
}


function Layout() {
  return (
    <div className="desktop">
      <header className="header">
        <div className="header-top">
          <nav className="utility-nav" aria-label="Utility Navigation">
            <a href="https://deutsch.hufs.ac.kr/sites/deutsch/index.do">독일어과 home</a>
            <a href="https://www.hufs.ac.kr/sites/hufs/index.do">HUFS home</a>
            <a href="#">언어 설정</a>
            <a href="#">로그인/회원가입</a>
          </nav>
        </div>
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
            <a href="#">도서관 소개</a>
          </nav>
        </div>
      </header>
      <Outlet /> {/* This will render the matched child route component */}
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

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="info" element={<Info />} />
      </Route>
    </Routes>
  );
}

export default App;