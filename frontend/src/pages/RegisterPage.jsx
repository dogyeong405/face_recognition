import { useState } from 'react';
import WebcamCapture from '../components/WebcamCapture';
import { registerFace } from '../api';

/**
 * 얼굴 등록 페이지
 * - 이름 입력
 * - 웹캠으로 사진 촬영 (여러 장 가능)
 * - 등록 API 호출
 */
function RegisterPage() {
    const [name, setName] = useState('');
    const [capturedImages, setCapturedImages] = useState([]);
    const [isRegistering, setIsRegistering] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleCapture = (blob) => {
        if (blob) {
            const url = URL.createObjectURL(blob);
            setCapturedImages(prev => [...prev, { blob, url }]);
        }
    };

    const removeImage = (index) => {
        setCapturedImages(prev => {
            const updated = [...prev];
            URL.revokeObjectURL(updated[index].url);
            updated.splice(index, 1);
            return updated;
        });
    };

    const handleRegister = async () => {
        if (!name.trim()) {
            setError('이름을 입력해주세요.');
            return;
        }
        if (capturedImages.length === 0) {
            setError('사진을 최소 1장 이상 촬영해주세요.');
            return;
        }

        setIsRegistering(true);
        setError(null);
        setResult(null);

        try {
            const files = capturedImages.map((img, i) => {
                return new File([img.blob], `face_${i}.jpg`, { type: 'image/jpeg' });
            });
            const response = await registerFace(name.trim(), files);
            setResult(response);
            // 성공 시 초기화
            setCapturedImages([]);
            setName('');
        } catch (err) {
            setError(err.response?.data?.detail || '등록 중 오류가 발생했습니다.');
        } finally {
            setIsRegistering(false);
        }
    };

    return (
        <div className="page register-page">
            <h2>📝 얼굴 등록</h2>

            <div className="register-form">
                <div className="input-group">
                    <label htmlFor="name-input">이름</label>
                    <input
                        id="name-input"
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="등록할 이름을 입력하세요"
                        className="text-input"
                    />
                </div>

                <WebcamCapture onCapture={handleCapture} />

                {capturedImages.length > 0 && (
                    <div className="captured-images">
                        <h3>촬영된 사진 ({capturedImages.length}장)</h3>
                        <div className="image-grid">
                            {capturedImages.map((img, index) => (
                                <div key={index} className="captured-image-item">
                                    <img src={img.url} alt={`캡처 ${index + 1}`} />
                                    <button
                                        onClick={() => removeImage(index)}
                                        className="btn-remove"
                                        title="삭제"
                                    >
                                        ×
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {error && <div className="message error-message">❌ {error}</div>}
                {result && (
                    <div className="message success-message">
                        ✅ {result.message}
                    </div>
                )}

                <button
                    onClick={handleRegister}
                    disabled={isRegistering || !name.trim() || capturedImages.length === 0}
                    className="btn btn-primary btn-large"
                >
                    {isRegistering ? '등록 중...' : `등록하기 (${capturedImages.length}장)`}
                </button>
            </div>
        </div>
    );
}

export default RegisterPage;
