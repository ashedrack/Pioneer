import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import { Cancel, CheckCircle, Info } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { fetchScheduledActions } from '../../api/scheduler';
import { format } from 'date-fns';

const ScheduledActions: React.FC = () => {
  const { data: scheduledActions } = useQuery(['scheduledActions'], fetchScheduledActions);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'warning';
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Scheduled Actions
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Resource</TableCell>
                    <TableCell>Action</TableCell>
                    <TableCell>Scheduled Time</TableCell>
                    <TableCell>Expected Savings</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {scheduledActions?.map((action: any) => (
                    <TableRow key={action.id}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography variant="body2">{action.resource_id}</Typography>
                          <Tooltip title={action.resource_type}>
                            <Info fontSize="small" sx={{ ml: 1, color: 'action.disabled' }} />
                          </Tooltip>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={action.action_type}
                          size="small"
                          color={action.action_type === 'shutdown' ? 'error' : 'success'}
                        />
                      </TableCell>
                      <TableCell>
                        {format(new Date(action.scheduled_time), 'MMM dd, yyyy HH:mm')}
                      </TableCell>
                      <TableCell>${action.expected_savings.toFixed(2)}</TableCell>
                      <TableCell>
                        <Chip
                          label={action.status}
                          size="small"
                          color={getStatusColor(action.status)}
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" color="success">
                          <CheckCircle fontSize="small" />
                        </IconButton>
                        <IconButton size="small" color="error">
                          <Cancel fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default ScheduledActions;
