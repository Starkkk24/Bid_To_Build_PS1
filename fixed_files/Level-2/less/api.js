import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

export const submitBatch = async (batchData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/batch`, batchData);
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to submit batch';
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
