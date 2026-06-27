import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Check backend health
  async healthCheck() {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Backend is not running');
    }
  },

  // Index a website
  async ingestWebsite(url) {
    try {
      const response = await api.post('/ingest', null, {
        params: { url },
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data.error || 'Failed to index website');
      }
      throw new Error('Network error. Please check if the backend is running.');
    }
  },

  // Ask a question
  async askQuestion(question) {
    try {
      const response = await api.post('/ask', null, {
        params: { question },
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data.error || 'Failed to get answer');
      }
      throw new Error('Network error. Please check if the backend is running.');
    }
  },
};

export default apiService;
