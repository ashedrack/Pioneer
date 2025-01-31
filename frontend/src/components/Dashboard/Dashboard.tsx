import React from 'react';
import { Box, Grid } from '@mui/material';
import DashboardLayout from '../Layout/DashboardLayout';
import MetricsDashboard from './MetricsDashboard';
import CostAnalysis from './CostAnalysis';

const Dashboard: React.FC = () => {
  return (
    <DashboardLayout>
      <Box sx={{ flexGrow: 1, height: '100vh', overflow: 'auto', p: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <MetricsDashboard />
          </Grid>
          <Grid item xs={12}>
            <CostAnalysis />
          </Grid>
        </Grid>
      </Box>
    </DashboardLayout>
  );
};

export default Dashboard;
