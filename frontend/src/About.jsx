//======================================================================
//======================================================================
// 도서관 소개 
//======================================================================
//======================================================================

import React from 'react';
import myImage from '../img/confusion_matrix.png';

function About() {
  return (
    <main className="main-content about-page">
      <br /><br /><h1>도서관 소개</h1>
      <div className="about-section">
        <h2>도서관 소개</h2>
        <p>한국외국어대학교 서양어대학 독일어과 소속 오스트리아도서관 (Austrian Library, Österreichische Bibliothek)은 1982년 오스트리아 대사관으로부터 직접 독일어 서적 수천 권을 기증받으며 그 역사가 시작되었습니다.
          현재는 총 5,000여권 규모 서적으로 이루어진, 국내에 몇 안 되는 <strong>독일어권 어문학 전문 도서관</strong>입니다.
          <br />
          국내에서 쉬이 접할 수 없는 독일어 서적을 비치해놓음으로서 독일어권 문학,어학에 관한 한국외국어대학교 학생 및 교수님들의 학문 연구 증진에 기여하고 있습니다.
        </p>
      </div>
      <div className="introduce-section">
        {/*<h2>학과장님</h2>
        <p>조국현 교수님의 한마디</p>
        <br />*/}
        <h2>장은수교수님</h2>
        <p>제 00대 도서관장 (0000-0000)</p>
        <p>장은수 교수님의 한마디</p>
      </div>
      <br /><h1>기술 접목: 언어학과 AI</h1>
      <div className="tech-section">
        <p>2025년 오스트리아 도서관의 디지털화에 쓰인 여러가지 기술들을 소개합니다.</p>
        <br />

        <h2>1. 분야 분류기: mBERT fine-tuning을 이용한 subject classifier</h2>
        <br />
        <h3>서비스 링크</h3>
        <a href="https://huggingface.co/spaces/jsjang0104/book-genre-classifier-service">https://huggingface.co/spaces/jsjang0104/book-genre-classifier-service</a>
          <br />
          <br />
        <h3>도입 배경</h3>
        <p>기존에는 도서 목록 구축 과정에서 도서 분야를 사람이 직접 판단하여 수기로 입력해야했습니다.
          해당 업무 방식은 잦은 오류와 긴 소요시간 등의 문제를 야기했고, 이에 문제를 해결하고자 AI 모델을 학습시켜
          도서를 입력하는 사서들의 업무 난이도를 줄이고자 하였습니다.</p>
          <br />
        <h3>의의</h3>
          <p>오스트리아 도서관의 디지털화 과정 중 도서 주제 분류에 AI를 활용시킨 해당 사례는 
          우리 한국외국어대학교가 보유한 방대한 독일어 문헌 자산과 자연어처리(NLP) 기술(mBERT기반 fine-tuning)을 접목시킨 
          '디지털 인문학(Digital Humanities)'의 실증적 사례입니다. 
          외국어 데이터를 단순히 보관하는 것을 넘어,
          한국외국어대학교의 기존 정체성과 새로운 시대의 흐름인 인공지능 기술의 융합입니다.</p>
        <br />
        <h3>모델 학습</h3>
        <p>Berlin State Library 제공 다국어 도서 공개 데이터셋 28525개를 
          8:1:1 비율로 나눠 각각 training, evaluation, test로 사용하였습니다.
          Multiclass classification(class: 문학, 어학, 사회과학, 역사)를 목적으로 Task-specific Fine-tuning을 진행하였고,
          우리 도서관이 독일어 뿐 아니라 한국어, 영어, 라틴어 등 여러 언어의 도서를 소장하고 있는 점을 고려하여
          pretrained model로 다국어를 다룰 수 있는 mBERT를 사용하였습니다.
          추가로 학습 데이터 class의 불균형(역사 33.24%, 문학31.51%, 사회과학26.95%, 어학8.29%) 
          보완을 위해 어학 class에 가중치(각 클래스의 빈도수에 반비례)를 부여하였습니다.</p>
          <br />

          <p><strong>주요 성능 지표:</strong></p>
          <p>Accuracy(Overall) 0.7291</p>
          <p>F1-Score(Weighted) 0.7284</p>
          <p>F1-Score(Macro) 0.7262</p>
          <p>Precision(Weighted) 0.7314</p>
          <p>Recall(Weighted) 0.7291</p>
          <br />

          <p><strong>클래스별 F1-Score:</strong></p>
          <p>역사 (Geschichte): 0.6868</p>
          <p>문학 (Literatur): 0.7348</p>
          <p>사회과학 (Sozialwissenschaften): 0.7800</p>
          <p>어학 (Sprachwissenschaft): 0.7032</p>
          <br />

          <p><strong>Normalized Confusion Matrix:</strong></p>
          <img src={myImage} alt="Normalized Confusion Matrix" />
          <p>대각선 값 = Recall</p>
          <p>대각선이 아닌 값 = 오분류 비율 (Prediced Label / Actual Label)</p>
          <br />

          <p>'역사' 부문에서 모델의 오분류 정도가 큰 점을 고려, 분류 작업의 정확도 향상을 위하여 실제 inference에서는 
          confidence에 따른 오름차순 class 목록이 출력되어 사람이 직접 선택할 수 있는 구조입니다.</p>
          <br />
          저장된 가중치는 다음 링크에서 다운로드 받을 수 있습니다: 
          <a href="https://huggingface.co/jsjang0104/book-genre-classifier-bert">https://huggingface.co/jsjang0104/book-genre-classifier-bert</a>
          <br />

          <br />
        
        
        <br />
        <br />
        <h2>2. 청구 기호 생성가: 텍스트 전처리 및 hashlib 라이브러리를 이용한 고유 문자열 생성</h2>
        <br />
        <h3>도입 배경</h3>
        <p>도서 목록 구축 기존 과정에서는 분야와 마찬가지로 청구 기호 또한 사람이 직접 만들어내는 구조로서 긴 소요시간과 더불어 
          작업 난이도로 인해 긴 청구 기호 생성이 불가능하였습니다. 또한 만들어진 청구기호가 중복되는 경우도 많아 도서를 고유하게 분류하는 용도의 청구기호로서의 의의가 퇴색되었었습니다.
          해당 문제를 해결하고자 중복없이 도서의 모든 정보를 담아내는 문자열을 생성하는 도구를 개발하여 
          청구기호의 본질적 의의를 되찾고 도서 입력 업무 시간을 획기적으로 줄이고자 하였습니다.</p>
        <br />
        <h3>작동 원리</h3>
        <p>사용 언어: Python</p>
        <p>1. input: 도서의 제목,저자,위치,언어가 입력된 csv 파일</p>
        <p>2. 파일 내 모든 문자열을 전처리 (ä,ü,ö,ß를 영어식 표현 ae, ue, oe, ss로 매핑 및 한자를 한글로 매핑, 공백 제거, 소문자 변환)</p>
        <p>3. 제목 및 저자에 대하여 hashlib 라이브러리를 이용한 해시 생성 후 16진수를 10진수 변환, 이후 지정된 자릿수에 맞는 나머지 연산</p>
        <p>4. 딕셔너리를 이용하여 중복 도서에 대한 순서 부여 
          (Key: 튜플 (위치, 제목, 저자, 분야, 언어), Value: 현재까지 등장한 횟수)</p>
        <p>5. output: 기존 data 구조에 청구기호 열이 추가된 csv 파일</p>
        <br />
        <p>해당 파이썬 파일은 다음 링크에서 다운로드 받을 수 있습니다: 
        <a href="https://drive.google.com/file/d/1htjFnBmoWcSdOwK-XJWu4HcRhK68ZqGH/view?usp=drive_link">https://drive.google.com/file/d/1htjFnBmoWcSdOwK-XJWu4HcRhK68ZqGH/view?usp=drive_link</a></p>
        <br />
        <br />
        <br /><h1>Tech Stack</h1>
        <br />
        <h3>Development</h3>
        <p>Language: Python, JavaScript</p>
        <p>Frontend: React, CSS</p>
        <p>Backend: Django, Django Rest Framework</p>
        <p>Database: PostgreSQL</p>
        <br />
        <h3>Deployment & Infra</h3>
        <p>Frontend Hosting: Vercel</p>
        <p>Backend Hosting: Render</p>
        <p>Database Hosting: Neon DB</p>
        <p>Monitoring: Uptime Robot</p>
      </div>
    </main>
  );
}

export default About;
