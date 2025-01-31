import React, { useEffect } from 'react';
import { Box, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { useApi } from '../../hooks/useApi';
import { metricsApi } from '../../services/api';

const ResourceMetrics = ({ resourceId }) => {
  const { data, error, loading, execute: fetchMetrics } = useApi(metricsApi.getResourceMetrics);

  useEffect(() => {
    if (resourceId) {
      fetchMetrics(resourceId);
    }
  }, [resourceId, fetchMetrics]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Typography color="error">Error loading metrics: {error}</Typography>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Resource Metrics
        </Typography>
        <Box mt={2}>
          <Typography variant="body1">
            CPU Usage: {data.cpu_usage.toFixed(1)}%
          </Typography>
          <Typography variant="body1">
            Memory Usage: {data.memory_usage.toFixed(1)}%
          </Typography>
          <Typography variant="body1">
            Disk Usage: {data.disk_usage.toFixed(1)}%
          </Typography>
          <Typography variant="body1">
            Error Rate: {data.error_rate.toFixed(2)} errors/min
          </Typography>
          <Typography variant="body1">
            Latency: {data.latency.toFixed(2)}ms
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResourceMetrics;
