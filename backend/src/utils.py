"""
이미지 처리 유틸리티 모듈
- 업로드된 이미지 파일을 OpenCV 형식으로 변환
- 이미지 파일 저장/로드
"""
import cv2
import numpy as np
from io import BytesIO


def bytes_to_cv2_image(image_bytes: bytes) -> np.ndarray:
    """바이트 데이터를 OpenCV 이미지(BGR numpy array)로 변환"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("이미지를 디코딩할 수 없습니다.")
    return image


def cv2_image_to_bytes(image: np.ndarray, ext: str = ".jpg") -> bytes:
    """OpenCV 이미지를 바이트로 변환"""
    success, buffer = cv2.imencode(ext, image)
    if not success:
        raise ValueError("이미지를 인코딩할 수 없습니다.")
    return buffer.tobytes()
