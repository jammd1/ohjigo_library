// 도서관 소개

import React from 'react';
import locationGif from '../img/location.gif';

function About() {
  return (
    <main className="main-content about-page">
      <br /><br /><h1>도서관 소개</h1>
      <div className="about-section">
        <h2>도서관 역사</h2>
        <p>도서관 역사</p>
      </div>
      <div className="about-section">
        <h2>위치 안내</h2>
        <p>서울특별시 02450 동대문구 이문로 107 한국외국어대학교 서울캠퍼스 본관 301호</p>
        <p>Austrian Library, Hankuk University of Foreign Studies, 107, Imun-ro, Dongdaemun-gu, Seoul, 02450, Republic of Korea</p>
        <img src={locationGif} alt="도서관 위치 안내" style={{ marginTop: '20px', maxWidth: '100%' }} />
      </div>
      <div className="about-section">
        <h2>규정</h2>
        <p><strong>대출 가능 권수</strong></p>
        <p>전임교수, 비전임교수: 15권 (3개월)</p>
        <p>대학원생: 10권 (1개월)</p>
        <p>학부생, 졸업생: 5권 (2주)</p>
      </div>
    </main>
  );
}

export default About;
