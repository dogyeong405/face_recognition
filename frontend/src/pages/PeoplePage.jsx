import { useState, useEffect } from 'react';
import { getPeople } from '../api';

/**
 * 등록된 사용자 목록 페이지
 * - 이름, 등록된 사진 수, 대표 사진 표시
 */
function PeoplePage() {
    const [people, setPeople] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchPeople = async () => {
        setLoading(true);
        try {
            const data = await getPeople();
            setPeople(data.people || []);
        } catch (err) {
            setError('사용자 목록을 불러오는 중 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPeople();
    }, []);

    if (loading) return <div className="page"><p>로딩 중...</p></div>;

    return (
        <div className="page people-page">
            <div className="page-header">
                <h2>👥 등록된 사용자</h2>
                <button onClick={fetchPeople} className="btn btn-secondary">
                    🔄 새로고침
                </button>
            </div>

            {error && <p className="error-text">{error}</p>}

            {people.length === 0 ? (
                <div className="empty-state">
                    <p>등록된 사용자가 없습니다.</p>
                    <p className="hint">등록 페이지에서 새로운 얼굴을 등록해보세요.</p>
                </div>
            ) : (
                <div className="people-grid">
                    {people.map((person) => (
                        <div key={person.id} className="person-card">
                            <div className="person-thumbnail">
                                {person.thumbnail ? (
                                    <img
                                        src={`/api/images/${person.thumbnail}`}
                                        alt={person.name}
                                    />
                                ) : (
                                    <div className="no-image">👤</div>
                                )}
                            </div>
                            <div className="person-info">
                                <h3>{person.name}</h3>
                                <p>등록 사진: {person.image_count}장</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div className="total-count">
                총 {people.length}명 등록됨
            </div>
        </div>
    );
}

export default PeoplePage;
