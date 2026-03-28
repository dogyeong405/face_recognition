import { useRef, useState, useCallback, useEffect } from 'react';
import { recognizeFace } from '../api';

/**
 * 실시간 얼굴 인식 페이지
 * - 웹캠 피드 위에 바운딩 박스 + 이름 오버레이
 * - 일정 간격으로 프레임 캡처 → 백엔드 전송
 */
function RecognitionPage() {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const overlayCanvasRef = useRef(null);
    const intervalRef = useRef(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const [faces, setFaces] = useState([]);
    const [statusMsg, setStatusMsg] = useState('카메라를 시작하세요.');
    const [error, setError] = useState(null);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480, facingMode: 'user' },
                audio: false,
            });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setIsStreaming(true);
                setError(null);
                setStatusMsg('인식 중...');

                // 0.5초 간격으로 프레임 캡처 및 인식
                intervalRef.current = setInterval(captureAndRecognize, 500);
            }
        } catch (err) {
            setError('카메라에 접근할 수 없습니다.');
        }
    };

    const stopCamera = useCallback(() => {
        if (videoRef.current?.srcObject) {
            videoRef.current.srcObject.getTracks().forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
        setIsStreaming(false);
        setFaces([]);
        setStatusMsg('카메라를 시작하세요.');
    }, []);

    const captureAndRecognize = useCallback(async () => {
        if (!videoRef.current || !canvasRef.current) return;

        const video = videoRef.current;
        const canvas = canvasRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(async (blob) => {
            if (!blob) return;
            try {
                const result = await recognizeFace(blob);
                setFaces(result.faces || []);
                setStatusMsg(result.message || '');
            } catch (err) {
                // 네트워크 에러 등은 무시 (연속 요청이므로)
                console.error('Recognition error:', err);
            }
        }, 'image/jpeg', 0.8);
    }, []);

    // 오버레이 캔버스에 바운딩 박스 그리기
    useEffect(() => {
        if (!overlayCanvasRef.current || !videoRef.current) return;

        const overlay = overlayCanvasRef.current;
        const video = videoRef.current;
        overlay.width = video.videoWidth || 640;
        overlay.height = video.videoHeight || 480;

        const ctx = overlay.getContext('2d');
        ctx.clearRect(0, 0, overlay.width, overlay.height);

        faces.forEach((face) => {
            const { x1, y1, x2, y2 } = face.bbox;
            const isKnown = face.name !== 'Unknown';

            // 바운딩 박스
            ctx.strokeStyle = isKnown ? '#00ff88' : '#ff4444';
            ctx.lineWidth = 2;
            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

            // 상단 라벨 (이름)
            const label = isKnown
                ? `${face.name} (${(face.similarity * 100).toFixed(0)}%)`
                : 'Unknown';
            ctx.font = 'bold 14px Segoe UI';
            const textWidth = ctx.measureText(label).width;

            ctx.fillStyle = isKnown ? 'rgba(0, 255, 136, 0.8)' : 'rgba(255, 68, 68, 0.8)';
            ctx.fillRect(x1, y1 - 24, textWidth + 12, 24);

            ctx.fillStyle = isKnown ? '#000' : '#fff';
            ctx.fillText(label, x1 + 6, y1 - 7);

            // 하단 라벨 (나이/성별)
            const infoLabel = `${face.gender} / ${face.age}세`;
            ctx.font = '12px Segoe UI';
            const infoWidth = ctx.measureText(infoLabel).width;

            ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
            ctx.fillRect(x1, y2, infoWidth + 12, 22);

            ctx.fillStyle = '#fff';
            ctx.fillText(infoLabel, x1 + 6, y2 + 15);
        });
    }, [faces]);

    // 컴포넌트 언마운트 시 정리
    useEffect(() => {
        return () => stopCamera();
    }, [stopCamera]);

    return (
        <div className="page recognition-page">
            <h2>🎥 얼굴 인식</h2>
            <p className="status-text">{statusMsg}</p>
            {error && <p className="error-text">{error}</p>}

            <div className="recognition-view">
                <div className="video-container">
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="webcam-video"
                    />
                    <canvas ref={overlayCanvasRef} className="overlay-canvas" />
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                </div>

                <div className="recognition-controls">
                    {!isStreaming ? (
                        <button onClick={startCamera} className="btn btn-primary btn-large">
                            📷 카메라 시작
                        </button>
                    ) : (
                        <button onClick={stopCamera} className="btn btn-danger btn-large">
                            ⏹ 중지
                        </button>
                    )}
                </div>

                {faces.length > 0 && (
                    <div className="faces-list">
                        <h3>감지된 얼굴</h3>
                        {faces.map((face, i) => (
                            <div key={i} className={`face-result ${face.name !== 'Unknown' ? 'known' : 'unknown'}`}>
                                <div className="face-main-info">
                                    <span className="face-name">{face.name}</span>
                                    <span className="face-similarity">
                                        {(face.similarity * 100).toFixed(1)}%
                                    </span>
                                </div>
                                <div className="face-detail-info">
                                    <span>{face.gender}</span>
                                    <span>{face.age}세</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default RecognitionPage;
