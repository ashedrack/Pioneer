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

module.exports = app;
