import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Basic resource metrics interface
export interface ResourceMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_usage: number;
  error_rate: number;
  latency: number;
}

// Metrics API with only essential endpoints
export const metricsApi = {
  getResourceMetrics: async (resourceId: string): Promise<ResourceMetrics> => {
    const { data } = await api.get(`/api/v1/resources/${resourceId}/metrics`);
    return data;
  },
};

export default api;
