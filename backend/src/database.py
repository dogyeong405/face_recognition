"""
데이터 저장소 모듈
- 등록된 사용자 정보(이름, 임베딩, 이미지 경로)를 JSON + numpy 파일로 관리
- 한글 이름 UTF-8 처리
"""
import json
import os
import uuid
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_FILE = os.path.join(DATA_DIR, "people.json")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def _ensure_dirs():
    """필요한 디렉토리들을 생성"""
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)


def _load_db() -> dict:
    """people.json 로드. 없으면 빈 dict 반환"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_db(db: dict):
    """people.json 저장 (UTF-8, 한글 보존)"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def get_all_people() -> list:
    """등록된 모든 사용자 정보 조회"""
    db = _load_db()
    people = []
    for person_id, info in db.items():
        people.append({
            "id": person_id,
            "name": info["name"],
            "image_count": len(info.get("images", [])),
            "thumbnail": info.get("images", [None])[0],
        })
    return people


def register_person(name: str, embeddings: list[np.ndarray], image_bytes_list: list[bytes]) -> str:
    """
    새 사용자 등록 또는 기존 사용자에 이미지 추가
    - name: 사용자 이름 (한글 가능)
    - embeddings: 각 이미지에서 추출한 얼굴 임베딩 리스트
    - image_bytes_list: 원본 이미지 바이트 리스트
    """
    _ensure_dirs()
    db = _load_db()

    # 같은 이름의 기존 사용자 찾기
    person_id = None
    for pid, info in db.items():
        if info["name"] == name:
            person_id = pid
            break

    if person_id is None:
        person_id = str(uuid.uuid4())[:8]
        db[person_id] = {"name": name, "images": [], "embedding_files": []}

    # 이미지 및 임베딩 저장
    for i, (emb, img_bytes) in enumerate(zip(embeddings, image_bytes_list)):
        # 이미지 파일 저장 (파일명에 한글 사용 안 함)
        img_filename = f"{person_id}_{len(db[person_id]['images'])+1}.jpg"
        img_path = os.path.join(IMAGES_DIR, img_filename)
        with open(img_path, "wb") as f:
            f.write(img_bytes)

        # 임베딩 저장
        emb_filename = f"{person_id}_{len(db[person_id]['embedding_files'])+1}.npy"
        emb_path = os.path.join(EMBEDDINGS_DIR, emb_filename)
        np.save(emb_path, emb)

        db[person_id]["images"].append(img_filename)
        db[person_id]["embedding_files"].append(emb_filename)

    _save_db(db)
    return person_id


def load_all_embeddings() -> list[dict]:
    """
    등록된 모든 임베딩을 로드하여 반환
    Returns: [{"person_id": str, "name": str, "embedding": np.ndarray}, ...]
    """
    db = _load_db()
    results = []
    for person_id, info in db.items():
        for emb_file in info.get("embedding_files", []):
            emb_path = os.path.join(EMBEDDINGS_DIR, emb_file)
            if os.path.exists(emb_path):
                emb = np.load(emb_path)
                results.append({
                    "person_id": person_id,
                    "name": info["name"],
                    "embedding": emb,
                })
    return results


def get_image_path(filename: str) -> str:
    """이미지 파일의 절대 경로 반환"""
    return os.path.join(IMAGES_DIR, filename)
