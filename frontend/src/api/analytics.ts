import { api } from './index';

export interface CostAnalyticsData {
  ec2: number;
  rds: number;
  s3: number;
  lambda: number;
  savings_trend: Array<{
    x: string;
    y: number;
  }>;
}

export const fetchCostAnalytics = async (): Promise<CostAnalyticsData> => {
  const response = await api.get('/costs/analytics');
  return response.data;
};
