// 도서관 소개 페이지 - 틀 완료, 내용 수정 필요

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
        <h2>교수님 말씀</h2>
        <p><strong>??? 학과장님</strong></p>
        <p>??? 교수님의 한마디</p>
        <br />
        <p><strong>장은수 명예 교수님</strong></p>
        <p>제 n대 도서관장 (19?? - 19??)</p>
      </div>
      <div className="about-section">
        <h2>도서관 사진</h2>
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
