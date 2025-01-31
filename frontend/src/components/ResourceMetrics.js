import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';

const ResourceMetrics = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Resource Metrics
          </Typography>
          <Typography variant="body1">
            Resource metrics and monitoring dashboard will be displayed here.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default ResourceMetrics;
