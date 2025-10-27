import React from 'react';

function Info() {
  return (
    <main className="main-content info-page">
      <br /><br /><h1>도서관 안내</h1>
      <div className="info-section">
        <h2>이용 시간</h2>
        <p><strong>학기 중:</strong> 09:00 ~ 17:00</p>
        <p><strong>방학 중:</strong> 10:00 ~ 15:00</p>
        <p><strong>점심시간:</strong> 12:00 ~ 13:00</p>
        <p>※ 주말 및 공휴일은 휴관입니다.</p>
      </div>
      <div className="info-section">
        <h2>위치 안내</h2>
        <p>서울특별시 동대문구 이문로 107 한국외국어대학교 서울캠퍼스 본관 301호</p>
        <p>우편번호 02450</p>
      </div>
      <div className="info-section">
        <h2>규정</h2>
        <p>신분별 대출 가능 권수</p>
        <p>신분별 공간 대관 여부</p>
      </div>
    </main>
  );
}

export default Info;
