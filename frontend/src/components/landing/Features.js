import React from 'react';
import { Box, Container, Grid, Typography, Paper } from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import ScaleIcon from '@mui/icons-material/Scale';
import CloudQueueIcon from '@mui/icons-material/CloudQueue';
import ScheduleIcon from '@mui/icons-material/Schedule';
import SecurityIcon from '@mui/icons-material/Security';
import BugReportIcon from '@mui/icons-material/BugReport';

const features = [
  {
    title: 'AI-Powered Cost Optimization',
    description: 'Identify and eliminate unused resources to reduce cloud spend.',
    icon: <AutoFixHighIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Predictive Scaling',
    description: 'Automatically scale cloud resources up or down based on usage patterns.',
    icon: <ScaleIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Multi-Cloud Support',
    description: 'Works seamlessly across AWS, Google Cloud, and Azure.',
    icon: <CloudQueueIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Automated Scheduling',
    description: 'Stop, start, and resize cloud resources automatically to optimize costs.',
    icon: <ScheduleIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Security & Compliance',
    description: 'SOC 2 compliant with enterprise-grade security measures.',
    icon: <SecurityIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'AI Troubleshooting Assistant',
    description: 'Detects and resolves cloud infrastructure issues automatically.',
    icon: <BugReportIcon sx={{ fontSize: 40 }} />,
  },
];

const Features = () => {
  return (
    <Box
      sx={{
        py: 8,
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="lg">
        <Typography
          component="h2"
          variant="h3"
          align="center"
          color="text.primary"
          gutterBottom
        >
          Key Features
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Paper
                sx={{
                  p: 3,
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                  },
                }}
                elevation={2}
              >
                <Box sx={{ color: 'primary.main', mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography color="text.secondary">
                  {feature.description}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Features;
