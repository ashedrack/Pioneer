import React from 'react';
import { Box, Grid, Container } from '@mui/material';
import DashboardLayout from '../Layout/DashboardLayout';
import MetricsDashboard from './MetricsDashboard';
import CostOptimization from './CostOptimization';
import ProcessMonitor from './ProcessMonitor';
import { useLocation } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const location = useLocation();
  const path = location.pathname;

  const renderContent = () => {
    switch (path) {
      case '/cost-optimization':
        return <CostOptimization />;
      case '/processes':
        return <ProcessMonitor />;
      default:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <MetricsDashboard />
            </Grid>
          </Grid>
        );
    }
  };

  return (
    <DashboardLayout>
      <Box sx={{ flexGrow: 1, height: '100vh', overflow: 'auto' }}>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          {renderContent()}
        </Container>
      </Box>
    </DashboardLayout>
  );
};

export default Dashboard;
