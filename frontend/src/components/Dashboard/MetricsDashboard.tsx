import React from 'react';
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

// Mock data for metrics
const mockData = {
  utilization: [
    { timestamp: '2025-01-31T00:00:00Z', value: 75 },
    { timestamp: '2025-01-31T01:00:00Z', value: 78 },
    { timestamp: '2025-01-31T02:00:00Z', value: 82 },
    { timestamp: '2025-01-31T03:00:00Z', value: 85 },
    { timestamp: '2025-01-31T04:00:00Z', value: 80 },
    { timestamp: '2025-01-31T05:00:00Z', value: 77 },
    { timestamp: '2025-01-31T06:00:00Z', value: 73 },
  ],
  cost: [
    { month: '2024-12', actual: 11500, predicted: 12000 },
    { month: '2025-01', actual: 12300, predicted: 12800 },
    { month: '2025-02', actual: 0, predicted: 13200 },
    { month: '2025-03', actual: 0, predicted: 13500 },
  ],
  status: {
    ok: 85,
    warning: 10,
    error: 5,
  }
};

const MetricsDashboard: React.FC = () => {
  // Using mock data directly instead of API calls
  const metrics = mockData;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Metrics Dashboard
      </Typography>

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
                  value={metrics.status.ok}
                  color="success"
                  sx={{ my: 1 }}
                />
                <Typography variant="body2" color="text.secondary">
                  Warning State
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={metrics.status.warning}
                  color="warning"
                  sx={{ my: 1 }}
                />
                <Typography variant="body2" color="text.secondary">
                  Error State
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={metrics.status.error}
                  color="error"
                  sx={{ my: 1 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Utilization Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resource Utilization
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={metrics.utilization}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                    />
                    <YAxis domain={[0, 100]} />
                    <Tooltip
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                      formatter={(value: number) => [`${value}%`, 'Utilization']}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="value"
                      name="Utilization"
                      stroke="#8884d8"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Cost Analysis */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Cost Analysis
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={metrics.cost}>
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
      </Grid>
    </Box>
  );
};

export default MetricsDashboard;
