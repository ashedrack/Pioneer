import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Tooltip,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Chip,
  Stack,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  Warning,
  Info,
  CheckCircle,
  ArrowForward,
  ExpandMore,
  ExpandLess,
} from '@mui/icons-material';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip } from 'recharts';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import costOptimizationApi, {
  CostDistribution,
  ForecastData,
  Recommendation
} from '../../api/costOptimizationApi';

const CostOptimization: React.FC = () => {
  const [distribution, setDistribution] = useState<CostDistribution[]>([]);
  const [forecastData, setForecastData] = useState<ForecastData[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [selectedRecommendation, setSelectedRecommendation] = useState<Recommendation | null>(null);
  const [totalCost, setTotalCost] = useState<number>(0);
  const [potentialSavings, setPotentialSavings] = useState<number>(0);
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCostData();
  }, []);

  const fetchCostData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch cost distribution
      const distResponse = await costOptimizationApi.getCostDistribution();
      setDistribution(distResponse.data.data);
      setTotalCost(distResponse.data.total);

      // Fetch forecast data
      const forecastResponse = await costOptimizationApi.getCostForecast();
      setForecastData(forecastResponse.data.data);
      setPotentialSavings(forecastResponse.data.summary.potentialSavings);

      // Fetch recommendations
      const recsResponse = await costOptimizationApi.getRecommendations();
      setRecommendations(recsResponse.data.recommendations);
    } catch (err) {
      setError('Failed to fetch cost optimization data. Please try again later.');
      console.error('Error fetching cost data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCardExpand = (id: string) => {
    const newExpanded = new Set(expandedCards);
    if (expandedCards.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedCards(newExpanded);
  };

  const handleViewDetails = async (recommendation: Recommendation) => {
    try {
      const response = await costOptimizationApi.getRecommendationDetails(recommendation.id);
      setSelectedRecommendation(response.data);
      setDetailsDialogOpen(true);
    } catch (err) {
      console.error('Error fetching recommendation details:', err);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Cost Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Cost Distribution
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={distribution}
                    dataKey="value"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label
                  >
                    {distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
            </Box>
            <Typography variant="subtitle1" align="center" sx={{ mt: 2 }}>
              Total Cost: ${totalCost.toLocaleString()}
            </Typography>
          </Paper>
        </Grid>

        {/* Cost Forecast */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Cost Forecast
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={forecastData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <RechartsTooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#8884d8"
                    name="Actual"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="forecast"
                    stroke="#82ca9d"
                    name="Forecast"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                  />
                  <Line
                    type="monotone"
                    dataKey="optimized"
                    stroke="#ff7300"
                    name="Optimized"
                    strokeWidth={2}
                    strokeDasharray="3 3"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
            <Typography variant="subtitle1" align="center" sx={{ mt: 2 }}>
              Potential Monthly Savings: ${potentialSavings.toLocaleString()}
            </Typography>
          </Paper>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Cost Optimization Recommendations
            </Typography>
            <List>
              {recommendations.map((recommendation) => (
                <React.Fragment key={recommendation.id}>
                  <ListItem>
                    <Card sx={{ width: '100%' }}>
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Typography variant="h6" component="div">
                            {recommendation.title}
                          </Typography>
                          <Stack direction="row" spacing={1}>
                            <Chip
                              label={`$${recommendation.savings.toLocaleString()} savings`}
                              color="success"
                              size="small"
                            />
                            <Chip
                              label={recommendation.impact}
                              color={
                                recommendation.impact === 'High'
                                  ? 'error'
                                  : recommendation.impact === 'Medium'
                                  ? 'warning'
                                  : 'info'
                              }
                              size="small"
                            />
                            <IconButton
                              onClick={() => handleCardExpand(recommendation.id)}
                              size="small"
                            >
                              {expandedCards.has(recommendation.id) ? (
                                <ExpandLess />
                              ) : (
                                <ExpandMore />
                              )}
                            </IconButton>
                          </Stack>
                        </Box>
                        {expandedCards.has(recommendation.id) && (
                          <>
                            <Typography color="text.secondary" sx={{ mt: 2 }}>
                              {recommendation.description}
                            </Typography>
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="subtitle2">Affected Resources:</Typography>
                              <List dense>
                                {recommendation.resources.map((resource) => (
                                  <ListItem key={resource}>
                                    <ListItemIcon>
                                      <Info fontSize="small" />
                                    </ListItemIcon>
                                    <ListItemText primary={resource} />
                                  </ListItem>
                                ))}
                              </List>
                            </Box>
                            <Button
                              variant="outlined"
                              endIcon={<ArrowForward />}
                              onClick={() => handleViewDetails(recommendation)}
                              sx={{ mt: 2 }}
                            >
                              View Details
                            </Button>
                          </>
                        )}
                      </CardContent>
                    </Card>
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Recommendation Details Dialog */}
      <Dialog
        open={detailsDialogOpen}
        onClose={() => setDetailsDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedRecommendation && (
          <>
            <DialogTitle>{selectedRecommendation.title}</DialogTitle>
            <DialogContent>
              <Typography variant="subtitle1" gutterBottom>
                Implementation Steps:
              </Typography>
              <List>
                {selectedRecommendation.details?.implementation_steps.map((step, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText primary={step} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                Risks:
              </Typography>
              <List>
                {selectedRecommendation.details?.risks.map((risk, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Warning color="warning" />
                    </ListItemIcon>
                    <ListItemText primary={risk} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                Prerequisites:
              </Typography>
              <List>
                {selectedRecommendation.details?.prerequisites.map((prereq, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Info color="info" />
                    </ListItemIcon>
                    <ListItemText primary={prereq} />
                  </ListItem>
                ))}
              </List>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setDetailsDialogOpen(false)}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default CostOptimization;
