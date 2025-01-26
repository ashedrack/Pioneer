import axios from 'axios';

export const getResourceMetrics = () => {
    return axios.get('/resources/metrics');
};

export const collectLogs = (logData) => {
    return axios.post('/logs', logData);
};

export const getProcessData = () => {
    return axios.get('/processes');
};
