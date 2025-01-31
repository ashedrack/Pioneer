import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LogViewer from './components/LogViewer';
import ProcessMonitor from './components/ProcessMonitor';
import MetricsDashboard from './components/Dashboard/MetricsDashboard';

const express = require('express');
const cors = require('cors');
const metricsRoutes = require('./routes/metrics');

const app = express();

app.use(cors());
app.use(express.json());

// API Routes
app.use('/api/metrics', metricsRoutes);

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MetricsDashboard />} />
                <Route path="/logs" element={<LogViewer />} />
                <Route path="/processes" element={<ProcessMonitor />} />
            </Routes>
        </Router>
    );
};

export default App;
module.exports = app;
