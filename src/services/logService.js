import api from './api';

// Constants for log levels
export const LOG_LEVELS = {
    DEBUG: 'debug',
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error',
    CRITICAL: 'critical'
};

// Constants for log categories
export const LOG_CATEGORIES = {
    SYSTEM: 'system',
    SECURITY: 'security',
    PERFORMANCE: 'performance',
    USER_ACTIVITY: 'user_activity',
    OPTIMIZATION: 'optimization',
    BILLING: 'billing',
    INTEGRATION: 'integration'
};

class LogService {
    constructor() {
        this.buffer = [];
        this.bufferSize = 100;
        this.flushInterval = 5000; // 5 seconds
        this.tenant = null;
        this.correlationId = null;
        
        // Start periodic flush
        setInterval(() => this.flush(), this.flushInterval);
    }

    // Initialize the service with tenant information
    initialize(tenant, options = {}) {
        this.tenant = tenant;
        this.bufferSize = options.bufferSize || this.bufferSize;
        this.flushInterval = options.flushInterval || this.flushInterval;
        
        // Reset flush interval if changed
        if (options.flushInterval) {
            clearInterval(this.flushInterval);
            setInterval(() => this.flush(), this.flushInterval);
        }
    }

    // Set correlation ID for request tracing
    setCorrelationId(id) {
        this.correlationId = id;
    }

    // Create a structured log entry
    createLogEntry(level, message, category, metadata = {}) {
        return {
            timestamp: new Date().toISOString(),
            level,
            category,
            message,
            tenant: this.tenant,
            correlationId: this.correlationId,
            metadata: {
                ...metadata,
                environment: process.env.NODE_ENV,
                userAgent: navigator.userAgent,
                url: window.location.href
            }
        };
    }

    // Add log to buffer
    addToBuffer(logEntry) {
        this.buffer.push(logEntry);
        
        // Flush if buffer size exceeded
        if (this.buffer.length >= this.bufferSize) {
            this.flush();
        }
    }

    // Flush logs to server
    async flush() {
        if (this.buffer.length === 0) return;

        const logsToSend = [...this.buffer];
        this.buffer = [];

        try {
            await api.post('/logs/batch', {
                logs: logsToSend
            });
        } catch (error) {
            // On error, add logs back to buffer
            this.buffer = [...logsToSend, ...this.buffer].slice(-this.bufferSize);
            console.error('Failed to send logs:', error);
        }
    }

    // Public logging methods
    debug(message, category = LOG_CATEGORIES.SYSTEM, metadata = {}) {
        const logEntry = this.createLogEntry(LOG_LEVELS.DEBUG, message, category, metadata);
        this.addToBuffer(logEntry);
    }

    info(message, category = LOG_CATEGORIES.SYSTEM, metadata = {}) {
        const logEntry = this.createLogEntry(LOG_LEVELS.INFO, message, category, metadata);
        this.addToBuffer(logEntry);
    }

    warn(message, category = LOG_CATEGORIES.SYSTEM, metadata = {}) {
        const logEntry = this.createLogEntry(LOG_LEVELS.WARN, message, category, metadata);
        this.addToBuffer(logEntry);
    }

    error(message, category = LOG_CATEGORIES.SYSTEM, metadata = {}) {
        const logEntry = this.createLogEntry(LOG_LEVELS.ERROR, message, category, metadata);
        this.addToBuffer(logEntry);
        // Force flush on error
        this.flush();
    }

    critical(message, category = LOG_CATEGORIES.SYSTEM, metadata = {}) {
        const logEntry = this.createLogEntry(LOG_LEVELS.CRITICAL, message, category, metadata);
        this.addToBuffer(logEntry);
        // Force flush on critical
        this.flush();
    }

    // Security specific logging
    security(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.SECURITY, metadata);
    }

    // Performance specific logging
    performance(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.PERFORMANCE, metadata);
    }

    // User activity logging
    activity(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.USER_ACTIVITY, metadata);
    }

    // Optimization event logging
    optimization(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.OPTIMIZATION, metadata);
    }

    // Billing event logging
    billing(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.BILLING, metadata);
    }

    // Integration event logging
    integration(message, metadata = {}) {
        this.info(message, LOG_CATEGORIES.INTEGRATION, metadata);
    }

    // Process and analyze log data
    async analyze(params) {
        try {
            const response = await api.post('/logs/analyze', params);
            return response.data;
        } catch (error) {
            console.error('Log analysis failed:', error);
            throw error;
        }
    }

    // Search logs with advanced filtering
    async search(params) {
        try {
            const response = await api.get('/logs/search', { params });
            return response.data;
        } catch (error) {
            console.error('Log search failed:', error);
            throw error;
        }
    }

    // Export logs for compliance
    async export(params) {
        try {
            const response = await api.post('/logs/export', params, {
                responseType: 'blob'
            });
            return response.data;
        } catch (error) {
            console.error('Log export failed:', error);
            throw error;
        }
    }

    // Get log statistics
    async getStatistics(params) {
        try {
            const response = await api.get('/logs/statistics', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to get log statistics:', error);
            throw error;
        }
    }
}

// Create and export a singleton instance
const logService = new LogService();
export default logService;
