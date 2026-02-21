"""
얼굴 인식 시스템 - FastAPI 백엔드
API 엔드포인트:
  POST /register  - 얼굴 등록 (이름 + 이미지들)
  POST /recognize - 얼굴 인식 (이미지 → 이름)
  GET  /people    - 등록된 사용자 목록
  GET  /images/{filename} - 등록된 얼굴 이미지 조회
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Annotated
import os

from backend.src.face_engine import extract_embedding, detect_faces, recognize_from_embeddings
from backend.src.database import register_person, load_all_embeddings, get_all_people, get_image_path
from backend.src.utils import bytes_to_cv2_image

app = FastAPI(title="얼굴 인식 API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "얼굴 인식 API 서버가 실행 중입니다."}


@app.post("/register")
async def register_face(
    name: Annotated[str, Form()],
    files: list[UploadFile] = File(...),
):
    """
    얼굴 등록 API
    - name: 등록할 사용자 이름 (한글 가능)
    - files: 얼굴 이미지 파일들 (1개 이상)
    """
    if not name.strip():
        raise HTTPException(status_code=400, detail="이름을 입력해주세요.")
    if not files:
        raise HTTPException(status_code=400, detail="이미지 파일을 업로드해주세요.")

    embeddings = []
    image_bytes_list = []

    for file in files:
        contents = await file.read()
        try:
            image = bytes_to_cv2_image(contents)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"파일 '{file.filename}'을(를) 이미지로 읽을 수 없습니다."
            )

        embedding = extract_embedding(image)
        if embedding is None:
            raise HTTPException(
                status_code=400,
                detail=f"파일 '{file.filename}'에서 얼굴을 찾을 수 없습니다."
            )

        embeddings.append(embedding)
        image_bytes_list.append(contents)

    person_id = register_person(name.strip(), embeddings, image_bytes_list)

    return {
        "success": True,
        "person_id": person_id,
        "name": name.strip(),
        "registered_count": len(embeddings),
        "message": f"'{name.strip()}' 님의 얼굴 {len(embeddings)}장이 등록되었습니다."
    }


@app.post("/recognize")
async def recognize_face(
    file: UploadFile = File(...),
):
    """
    얼굴 인식 API
    - file: 인식할 얼굴 이미지 파일
    - 반환: 감지된 얼굴들의 이름, 좌표, 유사도
    """
    contents = await file.read()
    try:
        image = bytes_to_cv2_image(contents)
    except ValueError:
        raise HTTPException(status_code=400, detail="이미지를 읽을 수 없습니다.")

    faces = detect_faces(image)
    if not faces:
        return {"faces": [], "message": "얼굴이 감지되지 않았습니다."}

    registered = load_all_embeddings()
    results = []

    for face in faces:
        bbox = face.bbox.astype(int).tolist()
        match = recognize_from_embeddings(face.embedding, registered)
        results.append({
            "name": match["name"],
            "similarity": round(match["similarity"], 4),
            "bbox": {
                "x1": bbox[0],
                "y1": bbox[1],
                "x2": bbox[2],
                "y2": bbox[3],
            },
        })

    return {
        "faces": results,
        "message": f"{len(results)}개의 얼굴이 감지되었습니다.",
    }


@app.get("/people")
def list_people():
    """등록된 사용자 목록 조회"""
    people = get_all_people()
    return {"people": people, "total": len(people)}


@app.get("/images/{filename}")
def get_image(filename: str):
    """등록된 얼굴 이미지 파일 제공"""
    path = get_image_path(filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
    return FileResponse(path, media_type="image/jpeg")
