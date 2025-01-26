"""Resource scheduler module."""

import asyncio
import logging
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List

import boto3


class ResourceScheduler:
    """Schedules and manages resource actions."""

    def __init__(self, dynamodb=None):
        """Initialize scheduler with DynamoDB resource."""
        self.dynamodb = (
            dynamodb
            if dynamodb
            else boto3.resource("dynamodb", region_name="us-east-1")
        )
        self.schedules_table = self.dynamodb.Table("cloud_pioneer_schedules")
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._task = None

    async def start(self):
        """Start the scheduler."""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._process_schedules())
            self.logger.info("Resource scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        if self._running:
            self._running = False
            if self._task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
            self.logger.info("Resource scheduler stopped")

    async def _process_schedules(self):
        """Process scheduled actions."""
        while self._running:
            try:
                # Get current schedules
                now = datetime.now().isoformat()
                response = self.schedules_table.scan(
                    FilterExpression="scheduled_time <= :now",
                    ExpressionAttributeValues={":now": now},
                )

                # Process each scheduled action
                for item in response.get("Items", []):
                    try:
                        # Execute action
                        await self._execute_action(item)

                        # Delete processed schedule
                        self.schedules_table.delete_item(
                            Key={
                                "resource_id": item["resource_id"],
                                "scheduled_time": item["scheduled_time"],
                            }
                        )
                    except Exception as e:
                        self.logger.error(f"Failed to process schedule: {str(e)}")

            except Exception as e:
                self.logger.error(f"Error in schedule processing: {str(e)}")

            # Wait before next check
            await asyncio.sleep(60)

    async def _execute_action(self, schedule: Dict[str, Any]):
        """Execute a scheduled action."""
        try:
            resource_id = schedule["resource_id"]
            action = schedule["action"]

            # Log action execution
            self.logger.info(f"Executing {action} on {resource_id}")

            # TODO: Implement actual resource actions
            # This is a placeholder for actual AWS API calls
            pass

        except Exception as e:
            self.logger.error(f"Failed to execute action: {str(e)}")
            raise

    def schedule_action(self, schedule_data: Dict[str, Any]):
        """Schedule a resource action."""
        try:
            # Convert float values to Decimal
            if isinstance(schedule_data.get("metrics"), dict):
                for key, value in schedule_data["metrics"].items():
                    if isinstance(value, float):
                        schedule_data["metrics"][key] = Decimal(str(value))

            # Store in DynamoDB
            self.schedules_table.put_item(Item=schedule_data)

        except Exception as e:
            self.logger.error(f"Failed to schedule action: {str(e)}")
            raise

    def get_scheduled_actions(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get scheduled actions for a resource."""
        try:
            response = self.schedules_table.query(
                KeyConditionExpression="resource_id = :rid",
                ExpressionAttributeValues={":rid": resource_id},
            )
            return response.get("Items", [])

        except Exception as e:
            self.logger.error(f"Failed to get scheduled actions: {str(e)}")
            raise
