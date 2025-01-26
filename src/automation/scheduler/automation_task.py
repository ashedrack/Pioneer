"""
Automation task model for resource scheduling
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AutomationTask(BaseModel):
    """
    Represents a scheduled automation task for resource management
    """

    task_id: str
    resource_id: str
    action: str
    scheduled_time: datetime
    status: str = "pending"
    parameters: Optional[Dict[str, Any]] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True
