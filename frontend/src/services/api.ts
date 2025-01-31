import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// API response types
export interface UtilizationData {
  timestamp: string;
  value: number;
}

export interface CostData {
  month: string;
  actual: number;
  predicted: number;
}

export interface StatusData {
  ok: number;
  warning: number;
  no_data: number;
}

export interface ResourceMetrics {
  resource_id: string;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  error_rate: number;
  latency: number;
}

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request logging
api.interceptors.request.use(request => {
  console.log('Request:', {
    method: request.method,
    url: (request.baseURL || '') + request.url,
    headers: request.headers
  });
  return request;
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
  submitMetrics: (data: any) => api.post('/resources/metrics', data),
  getMetrics: (resourceId: string) => api.get<ResourceMetrics>(`/resources/metrics/${resourceId}`),
  scheduleAction: (data: any) => api.post('/resources/schedule', data),
  getSchedule: (resourceId: string) => api.get(`/resources/schedule/${resourceId}`),
  getRecommendations: (resourceId: string) => api.get(`/resources/recommendations/${resourceId}`),
};

// Metrics API
export const metricsApi = {
  getUtilizationTrend: () => api.get<UtilizationData[]>('/metrics/utilization/trend'),
  getCostAnalysis: () => api.get<CostData[]>('/metrics/cost/analysis'),
  getResourceStatus: () => api.get<StatusData>('/metrics/resource/status'),
  getResourceMetrics: (resourceId: string) => api.get<ResourceMetrics>(`/metrics/resource/${resourceId}`)
};

// Auth API
export const authApi = {
  login: (credentials: { email: string; password: string }) => 
    api.post('/auth/login', credentials),
  register: (userData: any) => api.post('/auth/register', userData),
  refreshToken: () => api.post('/auth/refresh'),
  logout: () => api.post('/auth/logout')
};

export default api;
