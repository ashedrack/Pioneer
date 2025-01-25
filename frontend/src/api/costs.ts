import { api } from './index';

export interface CostOptimizationData {
  costs: {
    compute: number;
    storage: number;
    network: number;
  };
  total_cost: number;
  potential_savings: number;
  savings_percentage: number;
  recommendations: Array<{
    id: string;
    title: string;
    description: string;
    impact: number;
  }>;
}

export const fetchCostOptimization = async (): Promise<CostOptimizationData> => {
  const response = await api.get('/costs/optimization');
  return response.data;
};
