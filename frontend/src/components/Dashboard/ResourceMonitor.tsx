import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Alert,
  LinearProgress,
  Tooltip,
  Card,
  CardContent,
  Badge,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Memory,
  Storage,
  NetworkCheck,
  Warning,
  CheckCircle,
  Notifications,
  NotificationsOff,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { metricsApi } from '../../services/api';

interface Alert {
  id: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
}

interface ResourceCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  unit?: string;
  thresholds?: {
    warning: number;
    critical: number;
  };
}

const ResourceMonitor: React.FC = () => {
  const [alertsEnabled, setAlertsEnabled] = useState(true);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [historicalData, setHistoricalData] = useState<any[]>([]);

  const { data, isLoading, error } = useQuery(
    ['resourceMetrics'],
    () => metricsApi.getResourceMetrics('overall'),
    {
      refetchInterval: 5000, // Refresh every 5 seconds
    }
  );

  // Simulate receiving alerts
  useEffect(() => {
    if (!alertsEnabled) return;

    const checkThresholds = () => {
      if (data) {
        if (data.cpu_usage > 80) {
          addAlert('warning', 'High CPU usage detected');
        }
        if (data.memory_usage > 85) {
          addAlert('error', 'Critical memory usage');
        }
        if (data.error_rate > 5) {
          addAlert('error', 'High error rate detected');
        }
      }
    };

    const interval = setInterval(checkThresholds, 10000);
    return () => clearInterval(interval);
  }, [data, alertsEnabled]);

  // Update historical data
  useEffect(() => {
    if (data) {
      setHistoricalData(prev => {
        const newData = [...prev, { timestamp: new Date().toISOString(), ...data }];
        return newData.slice(-30); // Keep last 30 data points
      });
    }
  }, [data]);

  const addAlert = (severity: Alert['severity'], message: string) => {
    const newAlert: Alert = {
      id: Date.now().toString(),
      severity,
      message,
      timestamp: new Date().toISOString(),
    };
    setAlerts(prev => [newAlert, ...prev].slice(0, 5)); // Keep last 5 alerts
  };

  const getStatusColor = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return 'error';
    if (value >= thresholds.warning) return 'warning';
    return 'success';
  };

  const ResourceCard: React.FC<ResourceCardProps> = ({
    title,
    value,
    icon,
    unit = '%',
    thresholds = { warning: 70, critical: 85 },
  }) => {
    const color = getStatusColor(value, thresholds);
    
    return (
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box display="flex" alignItems="center" gap={1}>
              {icon}
              <Typography variant="h6">{title}</Typography>
            </Box>
            <Typography variant="h4" color={`${color}.main`}>
              {value}{unit}
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={value}
            color={color}
            sx={{ mt: 2, height: 8, borderRadius: 4 }}
          />
        </CardContent>
      </Card>
    );
  };

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <LinearProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">Failed to load resource metrics</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Resource Monitor</Typography>
        <FormControlLabel
          control={
            <Switch
              checked={alertsEnabled}
              onChange={(e) => setAlertsEnabled(e.target.checked)}
            />
          }
          label="Alerts"
        />
      </Box>

      <Grid container spacing={3}>
        {/* Resource Cards */}
        <Grid item xs={12} md={6} lg={3}>
          <ResourceCard
            title="CPU Usage"
            value={data?.cpu_usage ?? 0}
            icon={<Memory color="primary" />}
          />
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <ResourceCard
            title="Memory Usage"
            value={data?.memory_usage ?? 0}
            icon={<Storage color="primary" />}
          />
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <ResourceCard
            title="Disk Usage"
            value={data?.disk_usage ?? 0}
            icon={<Storage color="primary" />}
          />
        </Grid>
        <Grid item xs={12} md={6} lg={3}>
          <ResourceCard
            title="Network Latency"
            value={data?.latency ?? 0}
            icon={<NetworkCheck color="primary" />}
            unit="ms"
            thresholds={{
              warning: 100,
              critical: 200
            }}
          />
        </Grid>

        {/* Historical Data Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Historical Metrics
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="timestamp"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="cpu_usage"
                  name="CPU Usage"
                  stroke="#8884d8"
                />
                <Line
                  type="monotone"
                  dataKey="memory_usage"
                  name="Memory Usage"
                  stroke="#82ca9d"
                />
                <Line
                  type="monotone"
                  dataKey="disk_usage"
                  name="Disk Usage"
                  stroke="#ffc658"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Alerts List */}
        {alertsEnabled && alerts.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Recent Alerts
              </Typography>
              <List>
                {alerts.map((alert) => (
                  <ListItem key={alert.id}>
                    <ListItemIcon>
                      {alert.severity === 'error' ? (
                        <Warning color="error" />
                      ) : (
                        <Warning color="warning" />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={alert.message}
                      secondary={new Date(alert.timestamp).toLocaleString()}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default ResourceMonitor;
