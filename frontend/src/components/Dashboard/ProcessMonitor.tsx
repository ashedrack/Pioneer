import React from 'react';
import { Paper, Typography } from '@mui/material';

const ProcessMonitor: React.FC = () => {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Process Monitor
      </Typography>
      <Typography variant="body1">
        Process monitor component is under development.
      </Typography>
    </Paper>
  );
};

export default ProcessMonitor;
