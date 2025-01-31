import React from 'react';
import { Box, Container, Stepper, Step, StepLabel, StepContent, Typography, Paper } from '@mui/material';
import CloudDoneIcon from '@mui/icons-material/CloudDone';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import BugReportIcon from '@mui/icons-material/BugReport';
import AutorenewIcon from '@mui/icons-material/Autorenew';

const steps = [
  {
    label: 'Connect Your Cloud',
    description: 'Securely link AWS, GCP, or Azure accounts.',
    icon: <CloudDoneIcon />,
  },
  {
    label: 'AI Analyzes Your Usage',
    description: 'Detects cost inefficiencies and underutilized resources.',
    icon: <AnalyticsIcon />,
  },
  {
    label: 'Troubleshooting AI Detects Issues',
    description: 'Automatically runs diagnostics and suggests fixes.',
    icon: <BugReportIcon />,
  },
  {
    label: 'Automate & Save',
    description: 'Set up auto-scaling, scheduling, and cost alerts.',
    icon: <AutorenewIcon />,
  },
];

const HowItWorks = () => {
  return (
    <Box
      sx={{
        py: 8,
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="md">
        <Typography
          component="h2"
          variant="h3"
          align="center"
          color="text.primary"
          gutterBottom
        >
          How It Works
        </Typography>
        <Paper 
          elevation={3}
          sx={{ 
            mt: 4,
            p: 4,
            borderRadius: 2,
          }}
        >
          <Stepper orientation="vertical">
            {steps.map((step, index) => (
              <Step key={index} active={true}>
                <StepLabel
                  StepIconComponent={() => (
                    <Box
                      sx={{
                        color: 'primary.main',
                        display: 'flex',
                        alignItems: 'center',
                      }}
                    >
                      {step.icon}
                    </Box>
                  )}
                >
                  <Typography variant="h6">{step.label}</Typography>
                </StepLabel>
                <StepContent>
                  <Typography color="text.secondary">{step.description}</Typography>
                </StepContent>
              </Step>
            ))}
          </Stepper>
        </Paper>
      </Container>
    </Box>
  );
};

export default HowItWorks;
