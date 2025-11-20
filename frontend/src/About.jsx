// 도서관 소개 페이지 - 틀 완료, 내용 수정 필요

import React from 'react';
import locationGif from '../img/location.gif';

function About() {
  return (
    <main className="main-content about-page">
      <br /><br /><h1>도서관 소개</h1>
      <div className="about-section">
        <h2>도서관 소개</h2>
        <p>한국외국어대학교 서양어대학 독일어과 소속 오스트리아도서관 (Austrian Library, Bibliothek der Österreich)은 1982년 오스트리아 대사관으로부터 00여권의 책을 기증받으며 그 역사가 시작되었습니다.
          현재는 총 4,000여권 규모 서적(독어 서적 0000권, 한국어 서적 0000권)으로 이루어진, 국내에 몇 안 되는 <strong>독일어권 어문학 전문 도서관</strong>입니다.
          <br />
          국내에서 쉬이 접할 수 없는 독어 서적을 비치해놓음으로서 독일어권 문학,어학에 관한 한국외국어 대학교 학생 및 교수님들의 학문 연구 증진에 기여하고 있습니다.
          <br />
          주한 오스트리아 대사 초청 (2020, 2025)
        </p>
      </div>
      <div className="about-section">
        <h2>오스트리아 대사관 추천사</h2>
        <p>이메일 예정 (안 됨 말고...)</p>
        <br />

        <h2>조국현 학과장님</h2>
        <p>조국현 교수님의 한마디</p>
        <br />

        <h2>장은수 명예 교수님</h2>
        <p>제 n대 도서관장 (19?? - 19??)
          <br />
          장은수 교수님의 한마디
        </p>

        <h2>홍구슬 교수님 교수님</h2>
        <p>제 n대 도서관장 (19?? - 19??)
          <br />
          홍구슬 교수님의 한마디
        </p>
      </div>
      <div className="about-section">
        <h2>도서관 사진</h2>
      </div>
    </main>
  );
}

export default About;
