import { useRef, useCallback, useState } from 'react';

/**
 * 웹캠 캡처 컴포넌트
 * - 브라우저 카메라 접근
 * - 실시간 비디오 스트림 표시
 * - 이미지 캡처 기능
 */
function WebcamCapture({ onCapture, autoCapture = false, captureInterval = 500 }) {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const intervalRef = useRef(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const [error, setError] = useState(null);

    const startCamera = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480, facingMode: 'user' },
                audio: false,
            });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setIsStreaming(true);
                setError(null);

                // 자동 캡처 모드 (인식 페이지용)
                if (autoCapture && onCapture) {
                    intervalRef.current = setInterval(() => {
                        captureFrame();
                    }, captureInterval);
                }
            }
        } catch (err) {
            setError('카메라에 접근할 수 없습니다. 권한을 확인해주세요.');
            console.error('Camera error:', err);
        }
    }, [autoCapture, captureInterval]);

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
    }, []);

    const captureFrame = useCallback(() => {
        if (!videoRef.current || !canvasRef.current) return null;

        const video = videoRef.current;
        const canvas = canvasRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        return new Promise((resolve) => {
            canvas.toBlob((blob) => {
                if (onCapture) onCapture(blob);
                resolve(blob);
            }, 'image/jpeg', 0.85);
        });
    }, [onCapture]);

    return (
        <div className="webcam-container">
            {error && <div className="webcam-error">{error}</div>}
            <div className="webcam-video-wrapper">
                <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="webcam-video"
                />
                <canvas ref={canvasRef} style={{ display: 'none' }} />
            </div>
            <div className="webcam-controls">
                {!isStreaming ? (
                    <button onClick={startCamera} className="btn btn-primary">
                        📷 카메라 시작
                    </button>
                ) : (
                    <>
                        <button onClick={stopCamera} className="btn btn-danger">
                            ⏹ 카메라 중지
                        </button>
                        {!autoCapture && (
                            <button onClick={captureFrame} className="btn btn-secondary">
                                📸 캡처
                            </button>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}

export default WebcamCapture;
