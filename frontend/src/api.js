import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// 얼굴 등록
export const registerFace = async (name, imageFiles) => {
    const formData = new FormData();
    formData.append('name', name);
    imageFiles.forEach((file) => {
        formData.append('files', file);
    });
    const response = await api.post('/register', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
};

// 얼굴 인식
export const recognizeFace = async (imageBlob) => {
    const formData = new FormData();
    formData.append('file', imageBlob, 'capture.jpg');
    const response = await api.post('/recognize', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
};

// 등록된 사람 목록 조회
export const getPeople = async () => {
    const response = await api.get('/people');
    return response.data;
};

export default api;
