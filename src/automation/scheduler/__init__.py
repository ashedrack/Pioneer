"""
Scheduler package for resource automation
"""

from .automation_task import AutomationTask
from .resource_scheduler import ResourceScheduler

"""Resource Scheduler Module"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3


class ResourceScheduler:
    """Handles scheduling of resource actions"""

    def __init__(self, dynamodb=None):
        """Initialize the scheduler"""
        self.dynamodb = dynamodb or boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("cloud_pioneer_schedules")

    def schedule_task(self, resource_id: str, action: str, scheduled_time: str) -> bool:
        """Schedule a task for a resource"""
        try:
            self.table.put_item(
                Item={
                    "resource_id": resource_id,
                    "scheduled_time": scheduled_time,
                    "action": action,
                    "status": "pending",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            return True
        except Exception as e:
            print(f"Error scheduling task: {e}")
            return False

    def get_task_status(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get status of scheduled tasks for a resource"""
        try:
            response = self.table.query(
                KeyConditionExpression="resource_id = :rid",
                ExpressionAttributeValues={":rid": resource_id},
            )
            return response.get("Items", [])
        except Exception as e:
            print(f"Error getting task status: {e}")
            return []

    def update_task_status(
        self, resource_id: str, scheduled_time: str, status: str
    ) -> bool:
        """Update status of a scheduled task"""
        try:
            self.table.update_item(
                Key={"resource_id": resource_id, "scheduled_time": scheduled_time},
                UpdateExpression="SET #s = :s",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":s": status},
            )
            return True
        except Exception as e:
            print(f"Error updating task status: {e}")
            return False

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks that are due for execution"""
        try:
            now = datetime.now(timezone.utc).isoformat()
            response = self.table.scan(
                FilterExpression="#s = :status AND scheduled_time <= :now",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":status": "pending", ":now": now},
            )
            return response.get("Items", [])
        except Exception as e:
            print(f"Error getting pending tasks: {e}")
            return []


__all__ = ["ResourceScheduler", "AutomationTask"]
