import React, { useEffect, useState } from 'react';
import { Box, Grid, Paper, Typography, Card, CardContent } from '@mui/material';
import { styled } from '@mui/material/styles';
import DashboardLayout from '../Layout/DashboardLayout';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { 
  ResourceMetrics, 
  ResourceStatus, 
  UtilizationData, 
  CostData,
  fetchOverallMetrics,
  fetchUtilizationTrend,
  fetchCostAnalysis,
  fetchResourceStatus
} from '../../api/metrics';

const MetricCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

const StyledValue = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginBottom: theme.spacing(1),
}));

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<ResourceMetrics | null>(null);
  const [utilizationData, setUtilizationData] = useState<UtilizationData[]>([]);
  const [costData, setCostData] = useState<CostData[]>([]);
  const [resourceStatus, setResourceStatus] = useState<ResourceStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsData, utilData, costAnalysis, statusData] = await Promise.all([
          fetchOverallMetrics(),
          fetchUtilizationTrend(),
          fetchCostAnalysis(),
          fetchResourceStatus(),
        ]);

        setMetrics(metricsData);
        setUtilizationData(utilData);
        setCostData(costAnalysis);
        setResourceStatus(statusData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading || !metrics || !resourceStatus) {
    return (
      <DashboardLayout>
        <Box sx={{ p: 3 }}>
          <Typography>Loading dashboard data...</Typography>
        </Box>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Box sx={{ flexGrow: 1, p: 3 }}>
        {/* Uptime Status */}
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Resource Optimization Status</Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Box>
                <Typography variant="subtitle1">Past 7 Days</Typography>
                <Typography variant="h4" color="success.main">99.99%</Typography>
                <Typography variant="caption">Resource utilization target met</Typography>
              </Box>
            </Grid>
            <Grid item xs={6}>
              <Box>
                <Typography variant="subtitle1">Past 30 Days</Typography>
                <Typography variant="h4" color="success.main">99.95%</Typography>
                <Typography variant="caption">Cost optimization target met</Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        {/* Key Metrics */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <MetricCard elevation={2}>
              <Typography variant="subtitle1">Resource Utilization</Typography>
              <StyledValue color="success.main">{metrics.cpu_usage.toFixed(1)}%</StyledValue>
            </MetricCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard elevation={2}>
              <Typography variant="subtitle1">Cost Savings</Typography>
              <StyledValue color="success.main">${metrics.cost_savings.toFixed(0)}</StyledValue>
            </MetricCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard elevation={2}>
              <Typography variant="subtitle1">Average Latency</Typography>
              <StyledValue color="warning.main">{metrics.latency.toFixed(2)}s</StyledValue>
            </MetricCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard elevation={2}>
              <Typography variant="subtitle1">Error Rate</Typography>
              <StyledValue color="error.main">{metrics.error_rate.toFixed(2)}%</StyledValue>
            </MetricCard>
          </Grid>
        </Grid>

        {/* Charts */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Resource Utilization Trend</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={utilizationData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                    />
                    <YAxis />
                    <Tooltip 
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                    />
                    <Line type="monotone" dataKey="value" stroke="#4caf50" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Cost Analysis</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={costData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="actual" fill="#4caf50" name="Actual Cost" />
                    <Bar dataKey="predicted" fill="#ff9800" name="Predicted Cost" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Resource Status */}
        <Paper sx={{ p: 2, mt: 3 }}>
          <Typography variant="h6" gutterBottom>Resource Status</Typography>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Box sx={{ bgcolor: 'warning.main', p: 2, borderRadius: 1, color: 'white' }}>
                <Typography variant="h4">{resourceStatus.warning}</Typography>
                <Typography>Warning</Typography>
              </Box>
            </Grid>
            <Grid item xs={4}>
              <Box sx={{ bgcolor: 'success.main', p: 2, borderRadius: 1, color: 'white' }}>
                <Typography variant="h4">{resourceStatus.ok}</Typography>
                <Typography>OK</Typography>
              </Box>
            </Grid>
            <Grid item xs={4}>
              <Box sx={{ bgcolor: 'grey.500', p: 2, borderRadius: 1, color: 'white' }}>
                <Typography variant="h4">{resourceStatus.no_data}</Typography>
                <Typography>No Data</Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </DashboardLayout>
  );
};

export default Dashboard;
