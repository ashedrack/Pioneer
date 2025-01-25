import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Warning,
  Lightbulb,
  Timeline
} from '@mui/icons-material';
import { ResponsiveHeatMap } from '@nivo/heatmap';
import { useQuery } from '@tanstack/react-query';
import { fetchAIInsights } from '../../api/insights';

const AIInsights: React.FC = () => {
  const { data: insights = { 
    recommendations: [],
    usage_patterns: [],
    model_metrics: {
      accuracy: 0,
      savings_rate: 0,
      false_positive_rate: 0
    }
  } } = useQuery(['aiInsights'], fetchAIInsights);

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'optimization':
        return <TrendingUp color="success" />;
      case 'warning':
        return <Warning color="error" />;
      case 'prediction':
        return <Timeline color="primary" />;
      default:
        return <Lightbulb color="info" />;
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              AI-Generated Insights
            </Typography>
            <List>
              {insights.recommendations.map((insight: any, index: number) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    {getInsightIcon(insight.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={insight.title}
                    secondary={insight.description}
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Resource Usage Patterns
            </Typography>
            <Box sx={{ height: 400 }}>
              <ResponsiveHeatMap
                data={insights.usage_patterns}
                margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
                axisTop={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: -90,
                  legend: '',
                  legendOffset: 46
                }}
                axisRight={null}
                axisBottom={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: -90,
                  legend: 'Hour of Day',
                  legendPosition: 'middle',
                  legendOffset: 46
                }}
                axisLeft={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Day of Week',
                  legendPosition: 'middle',
                  legendOffset: -40
                }}
                colors={{
                  type: 'sequential',
                  scheme: 'blues'
                }}
                emptyColor="#ffffff"
                borderColor="#ffffff"
                labelTextColor="#ffffff"
                animate={true}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Performance Metrics
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Typography variant="body2" color="textSecondary">
                  Prediction Accuracy
                </Typography>
                <Box display="flex" alignItems="center">
                  <Box width="100%" mr={1}>
                    <LinearProgress
                      variant="determinate"
                      value={insights.model_metrics.accuracy * 100}
                      color="primary"
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Box minWidth={35}>
                    <Typography variant="body2" color="textSecondary">
                      {`${(insights.model_metrics.accuracy * 100).toFixed(1)}%`}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="body2" color="textSecondary">
                  Resource Savings
                </Typography>
                <Box display="flex" alignItems="center">
                  <Box width="100%" mr={1}>
                    <LinearProgress
                      variant="determinate"
                      value={insights.model_metrics.savings_rate * 100}
                      color="success"
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Box minWidth={35}>
                    <Typography variant="body2" color="textSecondary">
                      {`${(insights.model_metrics.savings_rate * 100).toFixed(1)}%`}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="body2" color="textSecondary">
                  False Positive Rate
                </Typography>
                <Box display="flex" alignItems="center">
                  <Box width="100%" mr={1}>
                    <LinearProgress
                      variant="determinate"
                      value={insights.model_metrics.false_positive_rate * 100}
                      color="error"
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Box minWidth={35}>
                    <Typography variant="body2" color="textSecondary">
                      {`${(insights.model_metrics.false_positive_rate * 100).toFixed(1)}%`}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default AIInsights;
