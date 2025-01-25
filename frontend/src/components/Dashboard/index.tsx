import React from 'react';
import { Container, Grid, Typography, Paper } from '@mui/material';
import AIInsights from './AIInsights';
import ResourceMetrics from './ResourceMetrics';
import ScheduledActions from './ScheduledActions';
import CostOptimization from './CostOptimization';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Cloud Resource Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Resource Metrics */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <ResourceMetrics />
          </Paper>
        </Grid>

        {/* AI Insights */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <AIInsights />
          </Paper>
        </Grid>

        {/* Scheduled Actions */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <ScheduledActions />
          </Paper>
        </Grid>

        {/* Cost Optimization */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
            <CostOptimization />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
