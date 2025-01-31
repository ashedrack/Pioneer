import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, CircularProgress } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { metricsApi } from '../../services/api';

function StatusCard({ title, value, color }) {
  return (
    <Paper sx={{ p: 2, bgcolor: `${color}.light`, height: '100%' }}>
      <Typography variant="h6" gutterBottom color={`${color}.dark`}>
        {title}
      </Typography>
      <Typography variant="h3" color={`${color}.dark`}>
        {value}
      </Typography>
    </Paper>
  );
}

function MetricsDashboard() {
  const [utilizationData, setUtilizationData] = useState([]);
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch initial utilization history
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [historyRes, statusRes] = await Promise.all([
          metricsApi.getUtilizationHistory(),
          metricsApi.getResourceStatus()
        ]);
        setUtilizationData(historyRes.data);
        setStatusData(statusRes.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  // Set up real-time updates
  useEffect(() => {
    const updateData = async () => {
      try {
        const [utilizationRes, statusRes] = await Promise.all([
          metricsApi.getCurrentUtilization(),
          metricsApi.getResourceStatus()
        ]);

        setUtilizationData(prevData => {
          const newData = [...prevData, utilizationRes.data];
          return newData.slice(-50); // Keep last 50 data points
        });
        setStatusData(statusRes.data);
      } catch (err) {
        console.error('Error updating metrics:', err);
      }
    };

    const intervalId = setInterval(updateData, 5000); // Update every 5 seconds

    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Paper sx={{ p: 2, bgcolor: 'error.light' }}>
        <Typography color="error">Error: {error}</Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Resource Monitoring Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Status Cards */}
        <Grid item xs={12} md={4}>
          <StatusCard
            title="Healthy Resources"
            value={statusData?.healthy || 0}
            color="success"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <StatusCard
            title="Warning Resources"
            value={statusData?.warning || 0}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <StatusCard
            title="No Data Resources"
            value={statusData?.noData || 0}
            color="error"
          />
        </Grid>

        {/* Utilization Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Resource Utilization Trend
            </Typography>
            <Box sx={{ height: 400 }}>
              <ResponsiveContainer>
                <LineChart data={utilizationData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={(time) => new Date(time).toLocaleTimeString()}
                  />
                  <YAxis
                    domain={[0, 100]}
                    tickFormatter={(value) => `${value}%`}
                  />
                  <Tooltip
                    labelFormatter={(label) => new Date(label).toLocaleString()}
                    formatter={(value) => [`${value}%`, 'Utilization']}
                  />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#2196f3"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* System Metrics */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Metrics
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="subtitle1" color="textSecondary">
                  CPU Usage
                </Typography>
                <Typography variant="h5">
                  {statusData?.metrics?.cpuUsage || 0}%
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="subtitle1" color="textSecondary">
                  Memory Usage
                </Typography>
                <Typography variant="h5">
                  {statusData?.metrics?.memoryUsage || 0}%
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default MetricsDashboard;
