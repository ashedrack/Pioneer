import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';

const ProcessMonitor = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Process Monitor
          </Typography>
          <Typography variant="body1">
            Running processes and system monitoring information will be displayed here.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default ProcessMonitor;
