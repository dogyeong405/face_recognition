# 얼굴 인식 웹 대시보드

React + FastAPI + InsightFace를 사용한 실시간 얼굴 인식 웹 애플리케이션입니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | React 19, Vite 7, react-router-dom, Axios |
| Backend | Python, FastAPI, Uvicorn |
| AI Engine | InsightFace (buffalo_l 모델), ONNX Runtime |
| 데이터 저장 | JSON + NumPy (.npy) |

## 기능

- **얼굴 등록**: 이름 입력 후 웹캠으로 여러 장 촬영하여 등록
- **실시간 인식**: 웹캠 화면 위에 이름과 바운딩 박스 오버레이
- **사용자 목록**: 등록된 사람 카드 그리드, 대표 이미지 표시

## 프로젝트 구조

```
/
├── backend/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── src/
│   │   ├── face_engine.py   # InsightFace 모델 래퍼 (감지, 임베딩, 매칭)
│   │   ├── database.py      # JSON + .npy 기반 데이터 저장/로드
│   │   └── utils.py         # 이미지 바이트 ↔ OpenCV 변환
│   └── data/                # 등록된 이미지 및 임베딩 저장 (자동 생성)
│       ├── people.json
│       ├── images/
│       └── embeddings/
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # 라우팅 및 레이아웃
│   │   ├── api.js           # Axios API 호출 함수
│   │   ├── components/
│   │   │   └── WebcamCapture.jsx
│   │   └── pages/
│   │       ├── RecognitionPage.jsx
│   │       ├── RegisterPage.jsx
│   │       └── PeoplePage.jsx
│   └── vite.config.js       # 개발 서버 프록시 설정
└── requirements.txt
```

## 시작하기

### 1. 백엔드 실행

```bash
# 프로젝트 루트에서 실행
pip install -r requirements.txt

python -m uvicorn backend.main:app --reload
# → http://localhost:8000
# → Swagger UI: http://localhost:8000/docs
```

> InsightFace의 buffalo_l 모델은 첫 `/register` 또는 `/recognize` 요청 시 자동 다운로드됩니다.

### 2. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

Vite 개발 서버는 `/api/*` 요청을 `http://localhost:8000`으로 프록시합니다.

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/register` | 얼굴 등록 (Form-Data: `name`, `files[]`) |
| `POST` | `/recognize` | 얼굴 인식 (Form-Data: `file`) |
| `GET` | `/people` | 등록된 사용자 목록 |
| `GET` | `/images/{filename}` | 등록된 얼굴 이미지 제공 |

### `/recognize` 응답 예시

```json
{
  "faces": [
    {
      "name": "홍길동",
      "similarity": 0.8432,
      "bbox": { "x1": 120, "y1": 80, "x2": 280, "y2": 300 }
    }
  ],
  "message": "1개의 얼굴이 감지되었습니다."
}
```

## 주의사항

- **한글 이름**: 이미지 파일명 대신 UUID를 사용하고 `people.json`에서 이름을 관리하므로 한글 깨짐 없음
- **유사도 임계값**: `face_engine.py`의 `SIMILARITY_THRESHOLD = 0.4` (높을수록 엄격)
- **모델**: `buffalo_l` (ArcFace 기반 고성능 모델). CPU 실행 지원
