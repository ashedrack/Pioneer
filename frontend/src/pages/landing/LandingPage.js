import React from 'react';
import { Box, AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '../../components/common/ThemeToggle';
import Hero from '../../components/landing/Hero';
import Features from '../../components/landing/Features';
import WhyChooseUs from '../../components/landing/WhyChooseUs';
import HowItWorks from '../../components/landing/HowItWorks';
import Testimonials from '../../components/landing/Testimonials';
import Pricing from '../../components/landing/Pricing';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <Box>
      {/* Navigation */}
      <AppBar position="fixed" color="default" elevation={0}>
        <Container maxWidth="lg">
          <Toolbar disableGutters sx={{ justifyContent: 'space-between' }}>
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ display: 'flex', alignItems: 'center' }}
            >
              <Box
                component="img"
                src="/assets/logo.svg"
                alt="CloudPioneer AI"
                sx={{ 
                  height: 50,
                  mr: 1,
                  filter: 'drop-shadow(0 0 10px rgba(0, 242, 255, 0.3))'
                }}
              />
              <Typography
                variant="h6"
                noWrap
                sx={{
                  background: 'linear-gradient(45deg, #00f2ff 30%, #00a8ff 90%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 700,
                  letterSpacing: 1
                }}
              >
                CloudPioneer AI
              </Typography>
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <ThemeToggle />
              <Button
                variant="outlined"
                color="primary"
                onClick={() => navigate('/login')}
              >
                Sign In
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/signup')}
              >
                Get Started
              </Button>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      <Toolbar /> {/* Spacer for fixed AppBar */}

      {/* Main Content */}
      <main>
        <Hero />
        <Features />
        <WhyChooseUs />
        <HowItWorks />
        <Testimonials />
        <Pricing />

        {/* Final CTA */}
        <Box
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            py: 8,
            textAlign: 'center',
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="h4" component="h2" gutterBottom>
              Sign up today and start saving on your cloud costs while fixing issues faster!
            </Typography>
            <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/signup')}
                sx={{
                  bgcolor: 'white',
                  color: 'primary.main',
                  '&:hover': {
                    bgcolor: 'grey.100',
                  },
                }}
              >
                Try CloudPioneer AI Free
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/demo')}
                sx={{
                  color: 'white',
                  borderColor: 'white',
                  '&:hover': {
                    borderColor: 'grey.100',
                    bgcolor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                Request a Demo
              </Button>
            </Box>
          </Container>
        </Box>
      </main>

      {/* Footer */}
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: 'background.paper',
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright '}
            {new Date().getFullYear()}
            {' CloudPioneer AI. All rights reserved.'}
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage;
