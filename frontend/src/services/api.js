import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeQuery = async (question) => {
  try {
    const response = await api.post('/api/analyze', { question });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'API request failed');
    } else if (error.request) {
      throw new Error('No response from server. Is the backend running?');
    } else {
      throw new Error('Failed to send request');
    }
  }
};

export const getHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('Health check failed');
  }
};

export const getSchema = async () => {
  try {
    const response = await api.get('/api/schema');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch schema');
  }
};

export default api;
