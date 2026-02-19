# GitHub Issues & Milestones 계획 (React + FastAPI + InsightFace)

이 문서는 사용자 요구사항(React, FastAPI, InsightFace)을 반영한 GitHub 이슈 및 마일스톤 계획입니다.

## 🎯 Milestone 1: 환경 설정 및 기본 구조 (Setup & Architecture)
**목표:** Frontend(React/Vite)와 Backend(FastAPI)의 기본 프로젝트 구조를 생성하고 연동 환경을 구축합니다.
- [ ] **Issue 1: Backend 초기화 (FastAPI)**
    - Python 가상환경 및 `requirements.txt` 설정 (`fastapi`, `uvicorn`, `insightface`, `onnxruntime`, `opencv-python`)
    - FastAPI 기본 앱 구조 생성 (`main.py`) 및 Hello World 엔드포인트 테스트
    - CORS 설정 (Frontend 연동 대비)
- [ ] **Issue 2: Frontend 초기화 (React + Vite)**
    - `npm create vite@latest frontend -- --template react` 실행
    - 주요 패키지 설치 (`axios`, `react-router-dom`, `tailwindcss` 등)
    - 동작 확인 및 기본 레이아웃 구성

## 🎯 Milestone 2: 백엔드 & AI 엔진 개발 (Backend & AI)
**목표:** InsightFace를 활용한 얼굴 인식 로직과 REST API를 구현합니다.
- [ ] **Issue 3: InsightFace 모델 연동**
    - InsightFace 얼굴 감지 및 인식 모델 로드 모듈 구현 (`src/face_engine.py`)
    - 얼굴 임베딩 추출 및 유사도 계산 로직 구현
- [ ] **Issue 4: 얼굴 등록/관리 API 구현**
    - `POST /register`: 이름 + 이미지(들) 업로드 -> 임베딩 추출 -> 저장
    - 데이터 저장소 구현 (파일 시스템 또는 SQLite DB 활용)
    - 한글 이름 인코딩 문제 처리 (UTF-8)
    - 한 사람당 여러 장의 사진 등록 지원 로직
- [ ] **Issue 5: 얼굴 인식 API 구현**
    - `POST /recognize`: 이미지 업로드 -> 얼굴 감지 -> 등록된 DB와 비교 -> 결과(이름/Unknown) 반환

## 🎯 Milestone 3: 프론트엔드 개발 (Frontend Implementation)
**목표:** 웹캠 연동 및 사용자 UI를 완성합니다.
- [ ] **Issue 6: 웹캠 연동 및 캡처 컴포넌트**
    - 브라우저 `navigator.mediaDevices.getUserMedia` 활용
    - 실시간 비디오 스트림 표시 및 이미지 캡처 기능 구현
- [ ] **Issue 7: 얼굴 등록 UI 개발**
    - 사용자 이름 입력 폼
    - 캡처된 이미지 미리보기 및 "등록" 버튼 구현 (API 연동)
    - 다중 이미지 등록 UI 지원
- [ ] **Issue 8: 실시간 인식 및 결과 표시**
    - 일정 간격(또는 프레임별)으로 캡처 이미지를 Backend로 전송
    - 인식 결과(이름, 좌표)를 받아 비디오 위에 바운딩 박스/이름 오버레이
- [ ] **Issue 9: 등록된 사용자 목록 페이지**
    - 등록된 사람들의 이름과 대표 사진을 리스트 형태로 조회 및 표시

## 🎯 Milestone 4: 통합 및 문서화 (Integration & Docs)
**목표:** 전체 시스템 테스트 및 문서를 정리합니다.
- [ ] **Issue 10: 전체 통합 테스트**
    - Frontend-Backend 연동 시나리오 테스트 (등록 -> 인식)
    - 예외 처리 (얼굴 미검출, 서버 오류 등)
- [ ] **Issue 11: 문서화 (README.md)**
    - 실행 방법 (Backend, Frontend 각각 실행 가이드)
    - API 명세 및 기술 스택 정리
