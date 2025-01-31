import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Resource Management API
export const resourceApi = {
  submitMetrics: (data) => api.post('/resources/metrics', data),
  getMetrics: (resourceId) => api.get(`/resources/metrics/${resourceId}`),
  scheduleAction: (data) => api.post('/resources/schedule', data),
  getSchedule: (resourceId) => api.get(`/resources/schedule/${resourceId}`),
  getRecommendations: (resourceId) => api.get(`/resources/recommendations/${resourceId}`),
};

// Metrics API
export const metricsApi = {
  getUtilizationTrend: () => api.get('/metrics/utilization'),
  getCostAnalysis: () => api.get('/metrics/cost'),
  getResourceStatus: () => api.get('/metrics/status'),
  getResourceMetrics: (resourceId) => api.get(`/metrics/resource/${resourceId}`),
};

// Auth API
export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  refreshToken: () => api.post('/auth/refresh'),
  logout: () => api.post('/auth/logout'),
};

export default api;
