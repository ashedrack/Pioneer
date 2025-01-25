import axios from 'axios';
import api from './axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Configure axios to include auth token
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface Metric {
  timestamp: string;
  metrics: {
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
    [key: string]: number;
  };
}

export interface MetricsResponse {
  status: string;
  data: {
    resource_id: string;
    metrics: Metric[];
  };
}

export const fetchResourceMetrics = async (resourceId: string = 'test-instance-1'): Promise<{
  metrics: Metric[];
  resource_id: string;
  timestamp: string;
  resourceMetrics?: Metric['metrics'];
}> => {
  const response = await api.get<MetricsResponse>(`${API_BASE_URL}/metrics/${resourceId}`);
  return {
    metrics: response.data?.data?.metrics || [],
    resource_id: resourceId,
    timestamp: new Date().toISOString(),
    resourceMetrics: response.data?.data?.metrics?.[0]?.metrics
  };
};

export const submitMetrics = async (resourceId: string, metrics: Metric['metrics']): Promise<void> => {
  await api.post(`${API_BASE_URL}/metrics`, {
    resource_id: resourceId,
    timestamp: new Date().toISOString(),
    metrics
  });
};

export interface Recommendation {
  resource_id: string;
  type: string;
  description: string;
  potential_savings: number;
  confidence: number;
}

export const fetchCostAnalytics = async (resourceId: string = 'test-instance-1'): Promise<Recommendation[]> => {
  const response = await api.get(`${API_BASE_URL}/recommendations/${resourceId}`);
  return response.data?.data || [];
};

export interface ScheduledAction {
  resource_id: string;
  action: string;
  scheduled_time: string;
  status: string;
}

export const fetchScheduledActions = async (resourceId: string = 'test-instance-1'): Promise<ScheduledAction[]> => {
  const response = await api.get(`${API_BASE_URL}/schedule/${resourceId}`);
  return response.data?.data || [];
};

export const scheduleAction = async (
  resourceId: string,
  action: string,
  scheduledTime: string
): Promise<void> => {
  await api.post(`${API_BASE_URL}/schedule`, {
    resource_id: resourceId,
    action,
    scheduled_time: scheduledTime
  });
};

export interface ResourceMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  cost_savings: number;
  error_rate: number;
  latency: number;
}

export interface ResourceStatus {
  warning: number;
  ok: number;
  no_data: number;
}

export interface UtilizationData {
  timestamp: string;
  value: number;
}

export interface CostData {
  month: string;
  actual: number;
  predicted: number;
}

export const fetchUtilizationTrend = async (): Promise<UtilizationData[]> => {
  const response = await api.get('/api/v1/metrics/utilization/trend');
  return response.data;
};

export const fetchCostAnalysis = async (): Promise<CostData[]> => {
  const response = await api.get('/api/v1/metrics/cost/analysis');
  return response.data;
};

export const fetchResourceStatus = async (): Promise<ResourceStatus> => {
  const response = await api.get('/api/v1/metrics/resource/status');
  return response.data;
};

export const fetchOverallMetrics = async (): Promise<ResourceMetrics> => {
  const response = await api.get('/api/v1/metrics/overall');
  return response.data;
};
