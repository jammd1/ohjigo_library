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
        <h2>학과장님 말씀</h2>
        <p>조국현 교수님의 한마디(?)</p>
      </div>
      <div className="about-section">
        <h2>도서 규모</h2>
        <p>독일어 서적</p>
        <p>한국어 서적</p>
        <p>독일어 영상 자료</p>
        <p>논문 등</p>
      </div>
    </main>
  );
}

export default About;
