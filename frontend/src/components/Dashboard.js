import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import TimelineIcon from '@mui/icons-material/Timeline';
import ListAltIcon from '@mui/icons-material/ListAlt';
import MonitorIcon from '@mui/icons-material/Monitor';
import LogoutIcon from '@mui/icons-material/Logout';
import ThemeToggle from './common/ThemeToggle';

// Import dashboard sub-components
import MetricsDashboard from './Dashboard/MetricsDashboard';
import LogViewer from './LogViewer';
import ProcessMonitor from './ProcessMonitor';

const DashboardHome = () => (
  <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
    <Grid container spacing={3}>
      {/* Welcome Message */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>
            Welcome to CloudPioneer AI
          </Typography>
          <Typography variant="body1">
            Monitor and optimize your cloud resources across AWS, GCP, and Azure.
          </Typography>
        </Paper>
      </Grid>

      {/* Metrics Dashboard */}
      <Grid item xs={12}>
        <MetricsDashboard />
      </Grid>
    </Grid>
  </Container>
);

const Dashboard = () => {
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'Metrics', icon: <TimelineIcon />, path: '/dashboard/metrics' },
    { text: 'Logs', icon: <ListAltIcon />, path: '/dashboard/logs' },
    { text: 'Processes', icon: <MonitorIcon />, path: '/dashboard/processes' },
  ];

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box
              component="img"
              src="/assets/logo.svg"
              alt="CloudPioneer AI"
              sx={{ 
                height: 40,
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
          </Box>
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        <ListItem button onClick={handleLogout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box
                component="img"
                src="/assets/logo.svg"
                alt="CloudPioneer AI"
                sx={{ 
                  height: 40,
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
            </Box>
          </Typography>
          <ThemeToggle />
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: 240 }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - 240px)` },
        }}
      >
        <Toolbar />
        <Routes>
          <Route path="/" element={<DashboardHome />} />
          <Route path="/metrics" element={<MetricsDashboard />} />
          <Route path="/logs" element={<LogViewer />} />
          <Route path="/processes" element={<ProcessMonitor />} />
        </Routes>
      </Box>
    </Box>
  );
};

export default Dashboard;
