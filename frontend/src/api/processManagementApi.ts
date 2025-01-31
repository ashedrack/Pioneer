import api from './api';

export interface Process {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error';
  cpu_usage: number;
  memory_usage: number;
  uptime: string;
}

export interface LogEntry {
  timestamp: string;
  level: 'INFO' | 'WARNING' | 'ERROR';
  message: string;
}

const processManagementApi = {
  getProcesses: () => api.get('/api/processes'),
  startProcess: (pid: string) => api.post(`/api/processes/${pid}/start`),
  stopProcess: (pid: string) => api.post(`/api/processes/${pid}/stop`),
  restartProcess: (pid: string) => api.post(`/api/processes/${pid}/restart`),
  getProcessLogs: (pid: string, lines: number = 100) => 
    api.get(`/api/processes/${pid}/logs`, { params: { lines } }),
};

export default processManagementApi;
