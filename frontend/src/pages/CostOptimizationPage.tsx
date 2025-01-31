import React from 'react';
import { Container } from '@mui/material';
import DashboardLayout from '../components/Layout/DashboardLayout';
import CostOptimization from '../components/Dashboard/CostOptimization';

const CostOptimizationPage: React.FC = () => {
  return (
    <DashboardLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <CostOptimization />
      </Container>
    </DashboardLayout>
  );
};

export default CostOptimizationPage;
