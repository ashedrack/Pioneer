import React from 'react';
import { Container, Grid, Paper, Box, Typography } from '@mui/material';
import ResourceMetrics from '../components/Dashboard/ResourceMetrics';
import CostAnalytics from '../components/Dashboard/CostAnalytics';
import ScheduledActions from '../components/Dashboard/ScheduledActions';
import AIInsights from '../components/Dashboard/AIInsights';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth={false}>
      <Box sx={{ py: 3 }}>
        <Typography variant="h4" gutterBottom>
          Cloud Resource Dashboard
        </Typography>
        
        <Grid container spacing={3}>
          {/* Resource Metrics Section */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h5" gutterBottom>
                Resource Utilization
              </Typography>
              <ResourceMetrics />
            </Paper>
          </Grid>

          {/* Cost Analytics Section */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h5" gutterBottom>
                Cost & Savings Analysis
              </Typography>
              <CostAnalytics />
            </Paper>
          </Grid>

          {/* AI Insights Section */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h5" gutterBottom>
                AI Insights & Predictions
              </Typography>
              <AIInsights />
            </Paper>
          </Grid>

          {/* Scheduled Actions Section */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h5" gutterBottom>
                Resource Management
              </Typography>
              <ScheduledActions />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;
