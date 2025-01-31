"""Process management routes."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
import psutil
import random

logger = logging.getLogger(__name__)
router = APIRouter()

def get_process_info(process: psutil.Process) -> Dict:
    """Get process information."""
    try:
        with process.oneshot():
            cpu_percent = process.cpu_percent(interval=0.1)
            memory_info = process.memory_info()
            create_time = datetime.fromtimestamp(process.create_time())
            uptime = str(timedelta(seconds=int((datetime.now() - create_time).total_seconds())))
            
            return {
                "id": str(process.pid),
                "name": process.name(),
                "status": "running",
                "cpu_usage": round(cpu_percent, 1),
                "memory_usage": round(memory_info.rss / (1024 * 1024), 1),  # Convert to MB
                "uptime": uptime
            }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

@router.get("/processes")
async def get_processes() -> Dict:
    """Get list of running processes."""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                process_info = get_process_info(proc)
                if process_info:
                    processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return {
            "processes": sorted(processes, key=lambda x: x["cpu_usage"], reverse=True)[:20]  # Return top 20 processes
        }
    except Exception as e:
        logger.error(f"Error getting processes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/processes/{pid}/start")
async def start_process(pid: int) -> Dict:
    """Start a process."""
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_STOPPED:
            process.resume()
            return {"message": f"Process {pid} started successfully"}
        return {"message": f"Process {pid} is already running"}
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        logger.error(f"Error starting process {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/processes/{pid}/stop")
async def stop_process(pid: int) -> Dict:
    """Stop a process."""
    try:
        process = psutil.Process(pid)
        process.suspend()
        return {"message": f"Process {pid} stopped successfully"}
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        logger.error(f"Error stopping process {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/processes/{pid}/restart")
async def restart_process(pid: int) -> Dict:
    """Restart a process."""
    try:
        process = psutil.Process(pid)
        process.suspend()
        process.resume()
        return {"message": f"Process {pid} restarted successfully"}
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        logger.error(f"Error restarting process {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processes/{pid}/logs")
async def get_process_logs(pid: int, lines: Optional[int] = 100) -> Dict:
    """Get process logs."""
    try:
        # Mock log data for demonstration
        log_entries = []
        timestamps = []
        current_time = datetime.now()
        
        for i in range(lines):
            timestamp = current_time - timedelta(seconds=i*30)
            timestamps.append(timestamp)
            
            # Generate different types of log messages
            if random.random() < 0.1:  # 10% chance for error
                level = "ERROR"
                message = f"Failed to complete operation: Error code {random.randint(1000, 9999)}"
            elif random.random() < 0.2:  # 20% chance for warning
                level = "WARNING"
                message = f"Resource usage high: {random.randint(80, 95)}% CPU utilization"
            else:  # 70% chance for info
                level = "INFO"
                message = f"Process operation completed successfully. Status: OK"
            
            log_entries.append({
                "timestamp": timestamp.isoformat(),
                "level": level,
                "message": message
            })
        
        return {
            "logs": sorted(log_entries, key=lambda x: x["timestamp"], reverse=True)
        }
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        logger.error(f"Error getting logs for process {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
