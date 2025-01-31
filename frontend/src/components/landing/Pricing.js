import React from 'react';
import { Box, Container, Typography, Card, CardContent, Button, Grid } from '@mui/material';
import SavingsIcon from '@mui/icons-material/Savings';
import BusinessIcon from '@mui/icons-material/Business';

const pricingOptions = [
  {
    title: 'Pay-as-You-Save',
    description: '10% of the savings identified by our AI',
    features: [
      'Full access to all features',
      'AI-powered cost optimization',
      'Real-time troubleshooting',
      'Multi-cloud support',
      'No upfront costs',
    ],
    icon: <SavingsIcon sx={{ fontSize: 40 }} />,
    buttonText: 'Get Started',
  },
  {
    title: 'Enterprise',
    description: 'Custom pricing for large organizations',
    features: [
      'Everything in Pay-as-You-Save',
      'Dedicated support team',
      'Custom integration options',
      'Advanced security features',
      'Volume discounts',
    ],
    icon: <BusinessIcon sx={{ fontSize: 40 }} />,
    buttonText: 'Contact Sales',
  },
];

const Pricing = () => {
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
          Pricing
        </Typography>
        <Typography
          variant="h6"
          align="center"
          color="text.secondary"
          paragraph
          sx={{ mb: 6 }}
        >
          Simple, transparent pricing that scales with your savings
        </Typography>
        <Grid container spacing={4} justifyContent="center">
          {pricingOptions.map((option, index) => (
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
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {option.icon}
                  </Box>
                  <Typography variant="h4" component="h3" gutterBottom>
                    {option.title}
                  </Typography>
                  <Typography
                    variant="h6"
                    color="text.secondary"
                    paragraph
                    sx={{ mb: 4 }}
                  >
                    {option.description}
                  </Typography>
                  <Box sx={{ mb: 4 }}>
                    {option.features.map((feature, featureIndex) => (
                      <Typography
                        key={featureIndex}
                        variant="body1"
                        color="text.secondary"
                        sx={{ mb: 1 }}
                      >
                        ✓ {feature}
                      </Typography>
                    ))}
                  </Box>
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    sx={{
                      mt: 'auto',
                    }}
                  >
                    {option.buttonText}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Pricing;
