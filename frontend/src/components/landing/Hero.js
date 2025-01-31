import React from 'react';
import { Box, Button, Container, Typography, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        bgcolor: 'background.paper',
        pt: 8,
        pb: 6,
      }}
    >
      <Container maxWidth="lg">
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
          sx={{ fontWeight: 'bold' }}
        >
          Cut Your Cloud Costs & Fix Issues Instantly with AI-Driven Optimization
        </Typography>
        <Typography variant="h5" align="center" color="text.secondary" paragraph>
          CloudPioneer AI helps businesses eliminate wasted cloud spend, automate resource management,
          and resolve cloud issues in real-time—all with zero manual effort.
        </Typography>
        <Stack
          sx={{ pt: 4 }}
          direction={{ xs: 'column', sm: 'row' }}
          spacing={2}
          justifyContent="center"
        >
          <Button 
            variant="contained" 
            size="large"
            onClick={() => navigate('/signup')}
            sx={{
              bgcolor: 'primary.main',
              '&:hover': {
                bgcolor: 'primary.dark',
              },
            }}
          >
            Try CloudPioneer AI for Free
          </Button>
          <Button 
            variant="outlined" 
            size="large"
            onClick={() => navigate('/demo')}
          >
            Watch Demo
          </Button>
        </Stack>
      </Container>
    </Box>
  );
};

export default Hero;
