import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Box,
  Chip,
  LinearProgress,
  Alert,
  Snackbar,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Refresh,
  Info,
  Warning,
  CheckCircle,
  Error,
} from '@mui/icons-material';
import processManagementApi, { Process, LogEntry } from '../../api/processManagementApi';

interface LogViewerDialogProps {
  open: boolean;
  onClose: () => void;
  processId: string;
  processName: string;
}

const LogViewerDialog: React.FC<LogViewerDialogProps> = ({
  open,
  onClose,
  processId,
  processName,
}) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open) {
      fetchLogs();
    }
  }, [open, processId]);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await processManagementApi.getProcessLogs(processId);
      setLogs(response.data.logs);
    } catch (err) {
      setError('Failed to fetch process logs');
      console.error('Error fetching logs:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        Logs for {processName} (PID: {processId})
      </DialogTitle>
      <DialogContent>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <Box sx={{ maxHeight: '400px', overflow: 'auto' }}>
            {logs.map((log, index) => (
              <Box
                key={index}
                sx={{
                  p: 1,
                  borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
                  '&:last-child': { borderBottom: 'none' },
                }}
              >
                <Typography variant="caption" color="textSecondary">
                  {new Date(log.timestamp).toLocaleString()}
                </Typography>
                <Chip
                  size="small"
                  label={log.level}
                  color={
                    log.level === 'ERROR'
                      ? 'error'
                      : log.level === 'WARNING'
                      ? 'warning'
                      : 'success'
                  }
                  sx={{ ml: 1, mr: 1 }}
                />
                <Typography variant="body2">{log.message}</Typography>
              </Box>
            ))}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        <Button onClick={fetchLogs} color="primary">
          Refresh
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const ProcessMonitor: React.FC = () => {
  const [processes, setProcesses] = useState<Process[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProcess, setSelectedProcess] = useState<Process | null>(null);
  const [logViewerOpen, setLogViewerOpen] = useState(false);
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error';
  }>({
    open: false,
    message: '',
    severity: 'success',
  });

  useEffect(() => {
    fetchProcesses();
    const interval = setInterval(fetchProcesses, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchProcesses = async () => {
    try {
      setError(null);
      const response = await processManagementApi.getProcesses();
      setProcesses(response.data.processes);
    } catch (err) {
      setError('Failed to fetch processes');
      console.error('Error fetching processes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProcessAction = async (
    action: 'start' | 'stop' | 'restart',
    process: Process
  ) => {
    try {
      let response;
      switch (action) {
        case 'start':
          response = await processManagementApi.startProcess(process.id);
          break;
        case 'stop':
          response = await processManagementApi.stopProcess(process.id);
          break;
        case 'restart':
          response = await processManagementApi.restartProcess(process.id);
          break;
      }
      
      setSnackbar({
        open: true,
        message: response.data.message,
        severity: 'success',
      });
      
      // Refresh process list
      fetchProcesses();
    } catch (err) {
      setSnackbar({
        open: true,
        message: `Failed to ${action} process: ${process.name}`,
        severity: 'error',
      });
      console.error(`Error ${action}ing process:`, err);
    }
  };

  const handleViewLogs = (process: Process) => {
    setSelectedProcess(process);
    setLogViewerOpen(true);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
        <Button
          color="inherit"
          size="small"
          onClick={fetchProcesses}
          sx={{ ml: 2 }}
        >
          Retry
        </Button>
      </Alert>
    );
  }

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">Process Monitor</Typography>
        <Button
          startIcon={<Refresh />}
          onClick={fetchProcesses}
          variant="outlined"
        >
          Refresh
        </Button>
      </Box>
      
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Process Name</TableCell>
              <TableCell>PID</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>CPU Usage</TableCell>
              <TableCell>Memory Usage</TableCell>
              <TableCell>Uptime</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {processes.map((process) => (
              <TableRow key={process.id}>
                <TableCell>{process.name}</TableCell>
                <TableCell>{process.id}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={process.status}
                    color={
                      process.status === 'running'
                        ? 'success'
                        : process.status === 'error'
                        ? 'error'
                        : 'warning'
                    }
                  />
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={process.cpu_usage}
                        color={
                          process.cpu_usage > 80
                            ? 'error'
                            : process.cpu_usage > 60
                            ? 'warning'
                            : 'primary'
                        }
                      />
                    </Box>
                    <Box sx={{ minWidth: 35 }}>
                      <Typography variant="body2" color="text.secondary">
                        {`${Math.round(process.cpu_usage)}%`}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>{`${process.memory_usage} MB`}</TableCell>
                <TableCell>{process.uptime}</TableCell>
                <TableCell>
                  <Tooltip title="Start Process">
                    <IconButton
                      size="small"
                      onClick={() => handleProcessAction('start', process)}
                      disabled={process.status === 'running'}
                    >
                      <PlayArrow />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Stop Process">
                    <IconButton
                      size="small"
                      onClick={() => handleProcessAction('stop', process)}
                      disabled={process.status === 'stopped'}
                    >
                      <Stop />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Restart Process">
                    <IconButton
                      size="small"
                      onClick={() => handleProcessAction('restart', process)}
                    >
                      <Refresh />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="View Logs">
                    <IconButton
                      size="small"
                      onClick={() => handleViewLogs(process)}
                    >
                      <Info />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {selectedProcess && (
        <LogViewerDialog
          open={logViewerOpen}
          onClose={() => setLogViewerOpen(false)}
          processId={selectedProcess.id}
          processName={selectedProcess.name}
        />
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default ProcessMonitor;
