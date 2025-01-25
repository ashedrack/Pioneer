import { api } from './index';

export interface AIInsight {
  recommendations: Array<{
    type: string;
    message: string;
    impact: string;
  }>;
  usage_patterns: Array<{
    id: string;
    data: Array<{
      x: string;
      y: number;
    }>;
  }>;
  model_metrics: {
    accuracy: number;
    savings_rate: number;
    false_positive_rate: number;
  };
}

export const fetchAIInsights = async (): Promise<AIInsight> => {
  const response = await api.get('/ai/insights');
  return response.data;
};
