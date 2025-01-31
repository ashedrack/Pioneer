import { addDays, subDays, startOfMonth, addMonths } from 'date-fns';

// Generate mock utilization data for the last 24 hours
export const mockUtilizationData = Array.from({ length: 24 }, (_, i) => ({
  timestamp: subDays(new Date(), 1).getTime() + i * 3600000,
  value: Math.floor(Math.random() * 40) + 30, // Random value between 30-70%
}));

// Generate mock cost data for the last 6 months
export const mockCostData = Array.from({ length: 6 }, (_, i) => {
  const date = startOfMonth(addMonths(new Date(), -5 + i));
  return {
    month: date.toISOString(),
    actual: Math.floor(Math.random() * 5000) + 5000, // Random value between 5000-10000
    predicted: Math.floor(Math.random() * 5000) + 5000,
  };
});

// Mock status data
export const mockStatusData = {
  ok: 12,
  warning: 3,
  no_data: 1,
};
