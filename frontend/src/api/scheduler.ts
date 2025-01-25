import { api } from './index';

export interface ScheduledAction {
  id: string;
  name: string;
  type: string;
  status: 'pending' | 'completed' | 'failed';
  scheduledTime: string;
  resource: string;
  details: string;
}

export const fetchScheduledActions = async (): Promise<ScheduledAction[]> => {
  const response = await api.get('/scheduler/actions');
  return response.data;
};
