import React from 'react';
import { Box, Container, Grid, Typography, Card, CardContent, Avatar } from '@mui/material';
import FormatQuoteIcon from '@mui/icons-material/FormatQuote';

const testimonials = [
  {
    quote: "CloudPioneer AI saved us 42% on AWS costs in the first month. Plus, their AI assistant diagnosed a configuration issue that took us days to find manually.",
    author: "CTO, TechCorp",
    avatar: "T",
  },
  {
    quote: "We no longer worry about cloud waste or unexpected outages. CloudPioneer AI does the work for us.",
    author: "Cloud Engineer, SaaS Inc.",
    avatar: "S",
  },
];

const Testimonials = () => {
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
          Customer Testimonials
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {testimonials.map((testimonial, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  overflow: 'visible',
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      position: 'absolute',
                      top: -20,
                      left: 20,
                      bgcolor: 'primary.main',
                      borderRadius: '50%',
                      width: 40,
                      height: 40,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <FormatQuoteIcon sx={{ color: 'white' }} />
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body1" paragraph sx={{ fontStyle: 'italic' }}>
                      {testimonial.quote}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                      <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>
                        {testimonial.avatar}
                      </Avatar>
                      <Typography variant="subtitle1" color="text.secondary">
                        {testimonial.author}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Testimonials;
