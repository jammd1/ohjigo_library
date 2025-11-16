// 도서관 안내 페이지 - 틀 완료, 내용 완료

import React from 'react';
import locationGif from '../img/location.gif';

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
        <p>서울특별시 02450 동대문구 이문로 107 한국외국어대학교 서울캠퍼스 본관 301호</p>
        <p>Austrian Library, Hankuk University of Foreign Studies, 107, Imun-ro, Dongdaemun-gu, Seoul, 02450, Republic of Korea</p>
        <img src={locationGif} alt="도서관 위치 안내" style={{ marginTop: '20px', maxWidth: '100%' }} />
      </div>
      <div className="info-section">
        <h2>규정</h2>
        <p><strong>대출 가능 권수</strong></p>
        <p>전임교수, 비전임교수: 15권 (3개월)</p>
        <p>대학원생: 10권 (1개월)</p>
        <p>학부생, 졸업생: 5권 (2주)</p>
        <br />
        <p><strong>기증 안내</strong></p>
        <p>도서 기증 문의: 독일어과 학과장실 이메일 (deutsch@hufs.ac.kr)에 하단 내용을 기입하여 문의 부탁드립니다.</p>
        <p>1. 성함, 신분, 연락처</p>
        <p>2. 도서 권종, 도서 규모</p>
      </div>
    </main>
  );
}

export default Info;
