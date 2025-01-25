import React from 'react';
import {
  Box,
  Grid,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
} from '@mui/material';
import { MonetizationOn, TrendingDown, SaveAlt } from '@mui/icons-material';
import { ResponsivePie } from '@nivo/pie';
import { useQuery } from '@tanstack/react-query';
import { fetchCostOptimization } from '../../api/costs';

const CostOptimization: React.FC = () => {
  const { data: costData } = useQuery(['costOptimization'], fetchCostOptimization);

  const pieData = [
    {
      id: 'compute',
      label: 'Compute',
      value: costData?.costs?.compute || 0,
      color: '#61cdbb',
    },
    {
      id: 'storage',
      label: 'Storage',
      value: costData?.costs?.storage || 0,
      color: '#97e3d5',
    },
    {
      id: 'network',
      label: 'Network',
      value: costData?.costs?.network || 0,
      color: '#e8c1a0',
    },
  ];

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Cost Optimization
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Box height={200}>
            <ResponsivePie
              data={pieData}
              margin={{ top: 10, right: 10, bottom: 10, left: 10 }}
              innerRadius={0.6}
              padAngle={0.7}
              cornerRadius={3}
              activeOuterRadiusOffset={8}
              colors={{ scheme: 'nivo' }}
              enableArcLinkLabels={false}
              arcLabelsSkipAngle={10}
            />
          </Box>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <List>
            <ListItem>
              <ListItemIcon>
                <MonetizationOn color="primary" />
              </ListItemIcon>
              <ListItemText
                primary="Total Cost"
                secondary={`$${costData?.total_cost || 0}`}
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <TrendingDown color="success" />
              </ListItemIcon>
              <ListItemText
                primary="Potential Savings"
                secondary={`$${costData?.potential_savings || 0}`}
              />
              <Chip
                label={`${costData?.savings_percentage || 0}%`}
                color="success"
                size="small"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <SaveAlt />
              </ListItemIcon>
              <ListItemText
                primary="Recommendations"
                secondary={costData?.recommendations?.length || 0}
              />
            </ListItem>
          </List>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CostOptimization;
