import React, { useMemo } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  addMonths,
  startOfMonth,
  endOfMonth,
  parseISO,
  isWithinInterval,
} from 'date-fns';

interface UtilizationData {
  timestamp: string;
  value: number;
}

interface CostData {
  month: string;
  actual: number;
  predicted: number;
}

interface StatusData {
  ok: number;
  warning: number;
  error: number;
}

// Mock data
const mockUtilizationData: UtilizationData[] = [
  { timestamp: '2025-01-31T00:00:00Z', value: 75 },
  { timestamp: '2025-01-31T01:00:00Z', value: 78 },
  { timestamp: '2025-01-31T02:00:00Z', value: 82 },
  { timestamp: '2025-01-31T03:00:00Z', value: 85 },
  { timestamp: '2025-01-31T04:00:00Z', value: 80 },
  { timestamp: '2025-01-31T05:00:00Z', value: 77 },
  { timestamp: '2025-01-31T06:00:00Z', value: 73 },
];

const mockCostData: CostData[] = [
  { month: '2024-12', actual: 11500, predicted: 12000 },
  { month: '2025-01', actual: 12300, predicted: 12800 },
  { month: '2025-02', actual: 0, predicted: 13200 },
  { month: '2025-03', actual: 0, predicted: 13500 },
];

const mockStatusData: StatusData = {
  ok: 85,
  warning: 10,
  error: 5,
};

const DashboardOverview: React.FC = () => {
  const startDate = startOfMonth(addMonths(new Date(), -2));
  const endDate = endOfMonth(addMonths(new Date(), 2));

  const utilizationData = mockUtilizationData;
  const rawCostData = mockCostData;
  const statusData = mockStatusData;

  const costData = useMemo(() => {
    if (!rawCostData) return [];
    return rawCostData.filter((item) => {
      const itemDate = parseISO(item.month);
      return isWithinInterval(itemDate, { start: startDate, end: endDate });
    });
  }, [rawCostData, startDate, endDate]);

  const currentUtilization = utilizationData && utilizationData.length > 0
    ? Math.round(
        utilizationData.slice(-5).reduce((acc, curr) => acc + curr.value, 0) / Math.min(5, utilizationData.length)
      )
    : 0;

  return (
    <Grid container spacing={3}>
      {/* Resource Status */}
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Resource Status
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Healthy Resources
              </Typography>
              <LinearProgress
                variant="determinate"
                value={statusData.ok}
                color="success"
                sx={{ my: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                Warning State
              </Typography>
              <LinearProgress
                variant="determinate"
                value={statusData.warning}
                color="warning"
                sx={{ my: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                Error State
              </Typography>
              <LinearProgress
                variant="determinate"
                value={statusData.error}
                color="error"
                sx={{ my: 1 }}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>

      {/* Current Utilization */}
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Current Utilization
            </Typography>
            <Typography variant="h3" component="div" sx={{ mb: 2 }}>
              {currentUtilization}%
            </Typography>
            <LinearProgress
              variant="determinate"
              value={currentUtilization}
              color={
                currentUtilization > 80
                  ? 'error'
                  : currentUtilization > 60
                  ? 'warning'
                  : 'success'
              }
            />
          </CardContent>
        </Card>
      </Grid>

      {/* Cost Trend */}
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Cost Trend
            </Typography>
            <Box sx={{ height: 200 }}>
              <ResponsiveContainer>
                <LineChart data={costData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="month"
                    tickFormatter={(value) => value.split('-')[1]}
                  />
                  <YAxis />
                  <Tooltip
                    formatter={(value: number) => [
                      `$${value.toLocaleString()}`,
                      'Cost',
                    ]}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    name="Actual Cost"
                    stroke="#82ca9d"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="predicted"
                    name="Predicted Cost"
                    stroke="#8884d8"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>
      </Grid>

      {/* Utilization Chart */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Utilization Trend
            </Typography>
            <Box sx={{ height: 400 }}>
              <ResponsiveContainer>
                <LineChart data={utilizationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                  />
                  <YAxis domain={[0, 100]} />
                  <Tooltip
                    labelFormatter={(value) =>
                      new Date(value).toLocaleString()
                    }
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="value"
                    name="Utilization %"
                    stroke="#8884d8"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default DashboardOverview;
