import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';

const LogViewer = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Log Viewer
          </Typography>
          <Typography variant="body1">
            System logs and events will be displayed here.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default LogViewer;
