import React from 'react';
import { Box, Card, CardContent, Grid, Typography, CircularProgress } from '@mui/material';
import { ResponsiveLine } from '@nivo/line';
import { useQuery } from '@tanstack/react-query';
import { fetchResourceMetrics } from '../../api/metrics';

const ResourceMetrics: React.FC = () => {
  const { data: metrics, isLoading, error } = useQuery(['resourceMetrics'], () => fetchResourceMetrics());

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <Typography color="error">Failed to load metrics</Typography>
      </Box>
    );
  }

  const formatMetricsData = (metricName: string) => {
    if (!metrics || !Array.isArray(metrics)) return [];
    
    return metrics
      .filter(m => m.metrics && m.metrics[metricName] !== undefined)
      .map(m => ({
        x: new Date(m.timestamp),
        y: m.metrics[metricName]
      }))
      .sort((a, b) => a.x.getTime() - b.x.getTime());
  };

  const cpuData = [
    {
      id: 'CPU Usage',
      data: formatMetricsData('cpu_usage')
    }
  ];

  const memoryData = [
    {
      id: 'Memory Usage',
      data: formatMetricsData('memory_usage')
    }
  ];

  const chartTheme = {
    axis: {
      ticks: {
        text: { fill: '#666' }
      },
      legend: {
        text: { fill: '#666' }
      }
    },
    grid: {
      line: { stroke: '#ddd', strokeDasharray: '2 4' }
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              CPU Usage
            </Typography>
            <Box sx={{ height: 300 }}>
              <ResponsiveLine
                data={cpuData}
                margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
                xScale={{
                  type: 'time',
                  format: 'native',
                  useUTC: false,
                  precision: 'minute',
                }}
                yScale={{
                  type: 'linear',
                  min: 0,
                  max: 100,
                }}
                axisBottom={{
                  format: '%H:%M',
                  tickRotation: -45,
                  legend: 'Time',
                  legendOffset: 40,
                }}
                axisLeft={{
                  legend: 'CPU Usage (%)',
                  legendOffset: -40,
                }}
                enablePoints={false}
                enableGridX={false}
                enableArea={true}
                areaOpacity={0.1}
                theme={chartTheme}
                curve="monotoneX"
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Memory Usage
            </Typography>
            <Box sx={{ height: 300 }}>
              <ResponsiveLine
                data={memoryData}
                margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
                xScale={{
                  type: 'time',
                  format: 'native',
                  useUTC: false,
                  precision: 'minute',
                }}
                yScale={{
                  type: 'linear',
                  min: 0,
                  max: 100,
                }}
                axisBottom={{
                  format: '%H:%M',
                  tickRotation: -45,
                  legend: 'Time',
                  legendOffset: 40,
                }}
                axisLeft={{
                  legend: 'Memory Usage (%)',
                  legendOffset: -40,
                }}
                enablePoints={false}
                enableGridX={false}
                enableArea={true}
                areaOpacity={0.1}
                theme={chartTheme}
                curve="monotoneX"
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default ResourceMetrics;
