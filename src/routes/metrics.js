const express = require('express');
const router = express.Router();
const os = require('os');

// Utility function to get CPU utilization
function getCpuUtilization() {
    const cpus = os.cpus();
    let totalIdle = 0;
    let totalTick = 0;

    cpus.forEach(cpu => {
        for (const type in cpu.times) {
            totalTick += cpu.times[type];
        }
        totalIdle += cpu.times.idle;
    });

    return {
        idle: totalIdle / cpus.length,
        total: totalTick / cpus.length
    };
}

// Store previous CPU measurements
let previousCpu = getCpuUtilization();
let utilizationHistory = [];
const MAX_HISTORY = 50; // Keep last 50 measurements

// Get current resource utilization
router.get('/utilization/current', (req, res) => {
    const currentCpu = getCpuUtilization();
    const idleDiff = currentCpu.idle - previousCpu.idle;
    const totalDiff = currentCpu.total - previousCpu.total;
    const utilization = 100 - Math.round(100 * idleDiff / totalDiff);
    
    previousCpu = currentCpu;
    
    const timestamp = new Date().toISOString();
    utilizationHistory.push({ timestamp, value: utilization });
    
    // Keep only the last MAX_HISTORY items
    if (utilizationHistory.length > MAX_HISTORY) {
        utilizationHistory = utilizationHistory.slice(-MAX_HISTORY);
    }
    
    res.json({ timestamp, value: utilization });
});

// Get utilization history
router.get('/utilization/history', (req, res) => {
    res.json(utilizationHistory);
});

// Get resource status
router.get('/status', (req, res) => {
    // Simulate resource status based on system metrics
    const memoryUsage = Math.round((1 - os.freemem() / os.totalmem()) * 100);
    const cpuUsage = Math.round(utilizationHistory.length > 0 ? 
        utilizationHistory[utilizationHistory.length - 1].value : 0);
    
    // Categorize resources based on usage thresholds
    const healthy = Math.round(Math.random() * 20) + 40; // 40-60 healthy resources
    const warning = Math.round(Math.random() * 10) + 5;  // 5-15 warning resources
    const noData = Math.round(Math.random() * 5);        // 0-5 no-data resources
    
    res.json({
        healthy,
        warning,
        noData,
        metrics: {
            memoryUsage,
            cpuUsage
        }
    });
});

module.exports = router;
