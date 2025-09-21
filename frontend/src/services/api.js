import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for LLM calls
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Generate risk profile from user answers
  generateProfile: async (answers) => {
    const response = await apiClient.post('/profile', { answers });
    return response.data;
  },

  // Get investment weights
  calculateWeights: async (label, variant, axes) => {
    const response = await apiClient.post('/weights', { label, variant, axes });
    return response.data;
  },

  // Run backtesting analytics
  runAnalytics: async (userWeights, label, axes) => {
    const response = await apiClient.post('/analytics', {
      user_weights: userWeights,
      label,
      axes
    });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  }
};

export default api;