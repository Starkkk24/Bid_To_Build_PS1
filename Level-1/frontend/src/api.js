import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const submitIDCard = async (formData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to submit ID card';
    }
};

export const fetchStatuses = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/status`);
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch statuses';
    }
};
