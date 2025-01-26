import axios from 'axios';

// API Configuration
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'https://api.cloudpioneer.com/v1',
    timeout: 30000,
});

// Request interceptor for API calls
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('cloudpioneer_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for API calls
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('cloudpioneer_refresh_token');
                const response = await api.post('/auth/refresh', { refreshToken });
                const { token } = response.data;
                
                localStorage.setItem('cloudpioneer_token', token);
                originalRequest.headers.Authorization = `Bearer ${token}`;
                
                return api(originalRequest);
            } catch (err) {
                // Redirect to login on refresh failure
                window.location.href = '/login';
                return Promise.reject(err);
            }
        }
        return Promise.reject(error);
    }
);

// Authentication APIs
export const auth = {
    login: (credentials) => api.post('/auth/login', credentials),
    register: (userData) => api.post('/auth/register', userData),
    logout: () => api.post('/auth/logout'),
    resetPassword: (email) => api.post('/auth/reset-password', { email }),
    verifyEmail: (token) => api.post('/auth/verify-email', { token }),
};

// Resource Management APIs
export const resources = {
    getMetrics: (params) => api.get('/resources/metrics', { params }),
    getOptimizationSuggestions: () => api.get('/resources/optimization'),
    applyOptimization: (resourceId, action) => 
        api.post(`/resources/${resourceId}/optimize`, { action }),
    forecast: (resourceId) => api.get(`/resources/${resourceId}/forecast`),
};

// Process Monitoring APIs
export const processes = {
    list: (params) => api.get('/processes', { params }),
    getDetails: (processId) => api.get(`/processes/${processId}`),
    stop: (processId) => api.post(`/processes/${processId}/stop`),
    restart: (processId) => api.post(`/processes/${processId}/restart`),
};

// Log Management APIs
export const logs = {
    collect: (logData) => api.post('/logs', logData),
    search: (params) => api.get('/logs/search', { params }),
    stream: (params) => api.get('/logs/stream', { 
        ...params,
        responseType: 'stream'
    }),
};

// Alert Management APIs
export const alerts = {
    list: () => api.get('/alerts'),
    create: (alertConfig) => api.post('/alerts', alertConfig),
    update: (alertId, config) => api.put(`/alerts/${alertId}`, config),
    delete: (alertId) => api.delete(`/alerts/${alertId}`),
    history: (params) => api.get('/alerts/history', { params }),
};

// Team Management APIs
export const teams = {
    list: () => api.get('/teams'),
    create: (teamData) => api.post('/teams', teamData),
    update: (teamId, data) => api.put(`/teams/${teamId}`, data),
    delete: (teamId) => api.delete(`/teams/${teamId}`),
    addMember: (teamId, userData) => api.post(`/teams/${teamId}/members`, userData),
    removeMember: (teamId, userId) => api.delete(`/teams/${teamId}/members/${userId}`),
};

// Billing APIs
export const billing = {
    getCurrentUsage: () => api.get('/billing/usage'),
    getInvoices: () => api.get('/billing/invoices'),
    updatePaymentMethod: (paymentData) => api.post('/billing/payment-method', paymentData),
    changePlan: (planId) => api.post('/billing/change-plan', { planId }),
};

// Integration APIs
export const integrations = {
    list: () => api.get('/integrations'),
    configure: (integrationType, config) => 
        api.post(`/integrations/${integrationType}`, config),
    test: (integrationType) => api.post(`/integrations/${integrationType}/test`),
    delete: (integrationType) => api.delete(`/integrations/${integrationType}`),
};

// Audit Log APIs
export const audit = {
    getLogs: (params) => api.get('/audit-logs', { params }),
    getEventTypes: () => api.get('/audit-logs/event-types'),
};

// Error handler helper
export const handleApiError = (error) => {
    const response = error.response;
    if (response?.status === 429) {
        return {
            error: 'Rate limit exceeded. Please try again later.',
            status: 429
        };
    }
    
    return {
        error: response?.data?.message || 'An unexpected error occurred',
        status: response?.status || 500
    };
};

// Export the configured axios instance
export default api;
