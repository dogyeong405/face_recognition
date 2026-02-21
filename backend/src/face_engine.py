"""
얼굴 인식 엔진 모듈
- InsightFace를 사용한 얼굴 감지/임베딩 추출
- 코사인 유사도 기반 얼굴 매칭
"""
import numpy as np
import insightface
from insightface.app import FaceAnalysis

# 전역 모델 인스턴스 (싱글톤)
_face_app = None
SIMILARITY_THRESHOLD = 0.4  # 유사도 임계값 (낮을수록 엄격)


def get_face_app() -> FaceAnalysis:
    """InsightFace 모델 로드 (최초 1회만)"""
    global _face_app
    if _face_app is None:
        _face_app = FaceAnalysis(name="buffalo_l")
        _face_app.prepare(ctx_id=0, det_size=(640, 640))
        print("InsightFace 모델 로드 완료")
    return _face_app


def detect_faces(image: np.ndarray) -> list:
    """
    이미지에서 얼굴을 감지하여 리스트로 반환
    각 얼굴 객체에는 bbox, embedding 등이 포함됨
    """
    app = get_face_app()
    faces = app.get(image)
    return faces


def extract_embedding(image: np.ndarray) -> np.ndarray | None:
    """
    이미지에서 가장 큰 얼굴의 임베딩을 추출
    얼굴이 없으면 None 반환
    """
    faces = detect_faces(image)
    if not faces:
        return None
    # 가장 큰 얼굴 선택 (bbox 면적 기준)
    largest_face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return largest_face.embedding


def compute_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """두 임베딩 간 코사인 유사도 계산"""
    emb1_norm = emb1 / np.linalg.norm(emb1)
    emb2_norm = emb2 / np.linalg.norm(emb2)
    return float(np.dot(emb1_norm, emb2_norm))


def recognize_from_embeddings(
    target_embedding: np.ndarray,
    registered: list[dict],
) -> dict:
    """
    타겟 임베딩을 등록된 임베딩들과 비교하여 가장 유사한 사람 찾기

    Args:
        target_embedding: 인식할 얼굴의 임베딩
        registered: [{"person_id", "name", "embedding"}, ...]

    Returns:
        {"name": str, "similarity": float, "person_id": str} 또는
        {"name": "Unknown", "similarity": 0.0, "person_id": None}
    """
    if not registered:
        return {"name": "Unknown", "similarity": 0.0, "person_id": None}

    best_match = {"name": "Unknown", "similarity": 0.0, "person_id": None}

    for entry in registered:
        sim = compute_similarity(target_embedding, entry["embedding"])
        if sim > best_match["similarity"]:
            best_match = {
                "name": entry["name"],
                "similarity": sim,
                "person_id": entry["person_id"],
            }

    if best_match["similarity"] < SIMILARITY_THRESHOLD:
        return {"name": "Unknown", "similarity": best_match["similarity"], "person_id": None}

    return best_match
