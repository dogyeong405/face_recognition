# 구현 계획 - 얼굴 인식 웹 대시보드 (React + FastAPI)

이 계획서는 **React** (Frontend), **FastAPI** (Backend), 그리고 **InsightFace** (AI Engine)를 사용하여 실시간 얼굴 인식 애플리케이션을 구축하는 단계를 설명합니다.

## 목표 설명 (Goal)
웹 브라우저(React)에서 웹캠을 구동하여 실시간으로 얼굴을 캡처하고, 백엔드(FastAPI)로 전송하여 얼굴을 인식하는 시스템입니다. InsightFace 모델을 활용하여 높은 정확도의 얼굴 인식 기능을 제공하며, 사용자 등록(다중 이미지) 및 관리 기능을 포함합니다.

## 사용자 검토 필요 사항
> [!IMPORTANT]
> **전체 아키텍처 변경**: 기존 Streamlit 단일 앱 구조에서 **Client-Server 구조**로 변경되었습니다.
> - **Frontend**: React + Vite (웹캠 제어, UI)
> - **Backend**: Python FastAPI (AI 모델 호스팅, REST API)
> - **Model**: InsightFace (ArcFace/Buffalo_L 등 고성능 모델 사용)

> [!NOTE]
> **한글 깨짐 문제**: 등록 시 한글 이름이 깨지는 문제를 방지하기 위해, 백엔드에서 UTF-8 인코딩 처리를 명확히 해야 합니다. 또한, 이미지 파일 저장 시 파일명에 한글을 쓰지 않고 매핑 테이블(DB/JSON)을 관리하는 방식을 권장합니다.

## 변경 제안 (Proposed Changes)

### 프로젝트 구조 (Project Structure)
```
/
├── backend/             # FastAPI 서버
│   ├── main.py          # API 진입점
│   ├── requirements.txt
│   ├── src/
│   │   ├── face_engine.py  # InsightFace 모델 래퍼
│   │   ├── database.py     # 데이터 저장/로드 (JSON/SQLite)
│   │   └── utils.py        # 이미지 처리 유틸리티
│   └── data/            # 등록된 얼굴 이미지 및 임베딩 저장소
│
└── frontend/            # React 앱 (Vite)
    ├── src/
    │   ├── components/  # Webcam, RegisterForm, FaceList 등
    │   ├── App.jsx      # 메인 라우팅 및 레이아웃
    │   └── api.py       # Axios API 호출 함수
    ├── package.json
    └── vite.config.js
```

### 1단계: 백엔드 구축 (FastAPI + InsightFace)
#### [NEW] [backend/src/face_engine.py]
- `insightface.app.FaceAnalysis` 초기화.
- `register_face(image, name)`: 얼굴 감지 -> 임베딩 추출 -> 저장.
- `recognize_face(image)`: 얼굴 감지 -> 임베딩 추출 -> 저장된 임베딩과 유사도 비교(Cosine Similarity) -> 가장 유사한 이름 반환.

#### [NEW] [backend/main.py]
- `POST /register`: Form-Data(이름, 이미지 파일들) 수신 -> 처리.
- `POST /recognize`: 이미지 파일 수신 -> 인식 결과(JSON) 반환.
- `GET /people`: 등록된 사람 목록 반환.

### 2단계: 프론트엔드 구축 (React + Vite)
#### [NEW] [frontend/src/components/WebcamCapture.jsx]
- `react-webcam` 또는 native `getUserMedia` API 사용.
- 캔버스에 비디오 스트림 렌더링.
- 주기적으로(예: 1초에 2~3회) 프레임 캡처 후 백엔드로 전송.

#### [NEW] [frontend/src/App.jsx]
- **등록 모드**: 이름 입력 필드 + 사진 촬영 버튼. 여러 장 촬영 후 일괄 등록 요청.
- **인식 모드**: 실시간 웹캠 화면 위에 인식된 이름과 바운딩 박스 오버레이(Canvas 활용).
- **목록 모드**: 등록된 사람 목록 및 대표 이미지 표시.

## 검증 계획 (Verification Plan)

### Back-end Test
- API 테스트 도구(Postman/Swagger UI)를 사용하여 `/register` 및 `/recognize` 엔드포인트 정상 동작 확인.
- 한글 이름 등록 후 조회 시 깨짐 없는지 확인.

### Front-end Test
- 웹캠 권한 요청 및 비디오 스트림 정상 출력 확인.
- 등록 프로세스 완료 후 "등록 성공" 메시지 확인.
- 인식 모드에서 등록된 얼굴 비출 시 올바른 이름 표시 확인.
