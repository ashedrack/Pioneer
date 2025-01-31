import React, { useEffect } from 'react';
import { Grid, Paper, Typography, CircularProgress, Box } from '@mui/material';
import { useApi } from '../../hooks/useApi';
import { metricsApi } from '../../services/api';

const MetricCard = ({ title, value, unit }) => (
  <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
    <Typography component="h2" variant="h6" color="primary" gutterBottom>
      {title}
    </Typography>
    <Typography component="p" variant="h4">
      {value} {unit}
    </Typography>
  </Paper>
);

const MetricsDashboard = () => {
  const {
    data: utilizationData,
    loading: utilizationLoading,
    error: utilizationError,
    execute: fetchUtilization
  } = useApi(metricsApi.getUtilizationTrend);

  const {
    data: costData,
    loading: costLoading,
    error: costError,
    execute: fetchCost
  } = useApi(metricsApi.getCostAnalysis);

  const {
    data: statusData,
    loading: statusLoading,
    error: statusError,
    execute: fetchStatus
  } = useApi(metricsApi.getResourceStatus);

  useEffect(() => {
    fetchUtilization();
    fetchCost();
    fetchStatus();
  }, [fetchUtilization, fetchCost, fetchStatus]);

  if (utilizationLoading || costLoading || statusLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <CircularProgress />
      </Box>
    );
  }

  if (utilizationError || costError || statusError) {
    return (
      <Paper sx={{ p: 2, bgcolor: 'error.light' }}>
        <Typography color="error">
          Error loading metrics: {utilizationError || costError || statusError}
        </Typography>
      </Paper>
    );
  }

  const latestUtilization = utilizationData?.[0]?.value || 0;
  const monthlyCost = costData?.[costData.length - 1]?.actual || 0;
  const resourceCount = statusData ? Object.values(statusData).reduce((a, b) => a + b, 0) : 0;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <MetricCard
          title="Resource Utilization"
          value={latestUtilization.toFixed(1)}
          unit="%"
        />
      </Grid>
      <Grid item xs={12} md={4}>
        <MetricCard
          title="Monthly Cost"
          value={`$${monthlyCost.toLocaleString()}`}
          unit=""
        />
      </Grid>
      <Grid item xs={12} md={4}>
        <MetricCard
          title="Total Resources"
          value={resourceCount}
          unit="active"
        />
      </Grid>
      
      {statusData && (
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Resource Status
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <Typography color="success.main" variant="h4">
                  {statusData.ok || 0}
                </Typography>
                <Typography variant="subtitle1">Healthy</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography color="warning.main" variant="h4">
                  {statusData.warning || 0}
                </Typography>
                <Typography variant="subtitle1">Warning</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography color="error.main" variant="h4">
                  {statusData.no_data || 0}
                </Typography>
                <Typography variant="subtitle1">No Data</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      )}
    </Grid>
  );
};

export default MetricsDashboard;
