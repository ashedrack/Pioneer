import React from 'react';
import { Container } from '@mui/material';
import DashboardLayout from '../components/Layout/DashboardLayout';
import ProcessMonitor from '../components/Dashboard/ProcessMonitor';

const ProcessMonitorPage: React.FC = () => {
  return (
    <DashboardLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <ProcessMonitor />
      </Container>
    </DashboardLayout>
  );
};

export default ProcessMonitorPage;
