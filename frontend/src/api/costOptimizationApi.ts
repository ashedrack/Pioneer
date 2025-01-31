import api from './api';

export interface CostDistribution {
  category: string;
  value: number;
  color: string;
}

export interface ForecastData {
  month: string;
  actual: number | null;
  forecast: number | null;
  optimized: number | null;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  impact: string;
  savings: number;
  effort: string;
  category: string;
  resources: string[];
  details?: {
    implementation_steps: string[];
    risks: string[];
    prerequisites: string[];
  };
}

const costOptimizationApi = {
  getCostDistribution: () => api.get('/api/cost-optimization/distribution'),
  getCostForecast: () => api.get('/api/cost-optimization/forecast'),
  getRecommendations: () => api.get('/api/cost-optimization/recommendations'),
  getRecommendationDetails: (id: string) => api.get(`/api/cost-optimization/recommendations/${id}`),
};

export default costOptimizationApi;
