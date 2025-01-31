import React from 'react';
import { Box, Container, Grid, Typography, Card, CardContent } from '@mui/material';
import SavingsIcon from '@mui/icons-material/Savings';
import AutomationIcon from '@mui/icons-material/AutoMode';
import CloudSyncIcon from '@mui/icons-material/CloudSync';
import SpeedIcon from '@mui/icons-material/Speed';

const reasons = [
  {
    title: 'Save 30-50% on Cloud Costs',
    description: 'Our AI-driven cost savings model ensures that you only pay for what you need—eliminating unnecessary expenses.',
    icon: <SavingsIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'No More Manual Optimization',
    description: 'Automate tedious cloud cost analysis and optimizations, freeing up DevOps and engineering teams.',
    icon: <AutomationIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Multi-Cloud, Fully Integrated',
    description: 'Unlike AWS Cost Explorer or Google Cloud Pricing Calculator, CloudPioneer AI works across all major cloud providers in a single dashboard.',
    icon: <CloudSyncIcon sx={{ fontSize: 40 }} />,
  },
  {
    title: 'Fix Cloud Issues Instantly',
    description: 'AI-powered troubleshooting assistant detects errors, runs diagnostics, and provides resolution steps in real-time.',
    icon: <SpeedIcon sx={{ fontSize: 40 }} />,
  },
];

const WhyChooseUs = () => {
  return (
    <Box
      sx={{
        py: 8,
        bgcolor: 'background.paper',
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
          Why Choose CloudPioneer AI?
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {reasons.map((reason, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                  },
                }}
              >
                <CardContent>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {reason.icon}
                  </Box>
                  <Typography variant="h5" component="h3" gutterBottom>
                    {reason.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {reason.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default WhyChooseUs;
