# 프로젝트 작업 목록: 얼굴 인식 웹 대시보드 (React + FastAPI)

- [ ] **프로젝트 환경 설정**
    - [ ] `backend` 폴더 생성 및 Python 가상환경 설정 (`fastapi`, `uvicorn`, `insightface`)
    - [/] Git 저장소 초기화 및 `.gitignore` 설정 (React, Python 통합)
    - [ ] `frontend` 폴더 생성 및 React Vite 프로젝트 초기화

- [ ] **백엔드 개발 (FastAPI + InsightFace)**
    - [ ] `backend/src/face_engine.py`: InsightFace 모델 로드 및 임베딩 추출 로직
    - [ ] `backend/main.py`: 얼굴 등록 API (`POST /register`) 구현 (다중 이미지 지원)
    - [ ] `backend/main.py`: 얼굴 인식 API (`POST /recognize`) 구현
    - [ ] 데이터 지속성 구현 (JSON/Pickle 또는 SQLite로 등록된 얼굴/이름 관리)

- [ ] **프론트엔드 개발 (React)**
    - [ ] 웹캠 컴포넌트 구현 (`react-webcam` 또는 native API)
    - [ ] 얼굴 등록 페이지 (이름 입력, 캡처, 전송)
    - [ ] 얼굴 인식 페이지 (실시간 프레임 전송 및 결과 오버레이)
    - [ ] 등록된 사용자 목록 페이지 (이름 및 대표 이미지 표시)

- [ ] **통합 및 테스트**
    - [ ] API 연동 테스트 (CORS 설정 확인)
    - [ ] 한글 이름 처리 검증
    - [ ] 전체 시나리오 테스트 (등록 -> 인식)

- [/] **Github 및 문서화**
    - [x] `PROJECT_PLAN.md` 및 `GITHUB_ISSUES.md` 업데이트
    - [x] GitHub Repository 생성 및 초기 커밋
    - [ ] `README.md` 작성 (실행 가이드 포함)
