/**
 * Format bytes to human readable format
 * @param {number} bytes - Number of bytes to format
 * @param {number} decimals - Number of decimal places to show
 * @returns {string} Formatted string (e.g., "1.5 GB")
 */
export const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

/**
 * Format uptime in seconds to human readable format
 * @param {number} seconds - Number of seconds to format
 * @returns {string} Formatted string (e.g., "2d 5h 30m")
 */
export const formatUptime = (seconds) => {
    if (!seconds) return '0s';

    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    const parts = [];

    if (days > 0) parts.push(`${days}d`);
    if (hours > 0) parts.push(`${hours}h`);
    if (minutes > 0) parts.push(`${minutes}m`);
    if (remainingSeconds > 0 && parts.length === 0) parts.push(`${remainingSeconds}s`);

    return parts.join(' ');
};

/**
 * Format date to human readable format
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
export const formatDate = (date) => {
    const d = new Date(date);
    return d.toLocaleString();
};

/**
 * Format percentage to string with specified decimals
 * @param {number} value - Value to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage string
 */
export const formatPercentage = (value, decimals = 1) => {
    return `${value.toFixed(decimals)}%`;
};

/**
 * Format currency value
 * @param {number} value - Value to format
 * @param {string} currency - Currency code (e.g., 'USD')
 * @returns {string} Formatted currency string
 */
export const formatCurrency = (value, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(value);
};

/**
 * Format number with thousand separators
 * @param {number} value - Value to format
 * @returns {string} Formatted number string
 */
export const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(value);
};

/**
 * Format time duration in milliseconds
 * @param {number} ms - Duration in milliseconds
 * @returns {string} Formatted duration string
 */
export const formatDuration = (ms) => {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    const minutes = Math.floor(ms / 60000);
    const seconds = ((ms % 60000) / 1000).toFixed(0);
    return `${minutes}m ${seconds}s`;
};

/**
 * Format file size for display in file browser
 * @param {number} size - Size in bytes
 * @returns {string} Formatted size string
 */
export const formatFileSize = (size) => {
    return formatBytes(size, 1);
};

/**
 * Format network speed (bytes per second)
 * @param {number} bytesPerSecond - Speed in bytes per second
 * @returns {string} Formatted speed string
 */
export const formatSpeed = (bytesPerSecond) => {
    return `${formatBytes(bytesPerSecond)}/s`;
};
