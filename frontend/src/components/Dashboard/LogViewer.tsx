import React from 'react';
import { Paper, Typography } from '@mui/material';

const LogViewer: React.FC = () => {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Log Viewer
      </Typography>
      <Typography variant="body1">
        Log viewer component is under development.
      </Typography>
    </Paper>
  );
};

export default LogViewer;
