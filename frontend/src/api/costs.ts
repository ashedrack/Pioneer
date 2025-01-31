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
  try {
    const response = await api.get('/costs/optimization');
    return response.data;
  } catch (error) {
    console.warn('Failed to fetch cost optimization data, using mock data:', error);
    // Return mock data for development
    return {
      costs: {
        compute: 1200,
        storage: 800,
        network: 400
      },
      total_cost: 2400,
      potential_savings: 600,
      savings_percentage: 25,
      recommendations: [
        {
          id: '1',
          title: 'Optimize compute resources',
          description: 'Consider right-sizing underutilized instances',
          impact: 300
        },
        {
          id: '2',
          title: 'Storage optimization',
          description: 'Move infrequently accessed data to lower-cost storage tiers',
          impact: 200
        }
      ]
    };
  }
};
