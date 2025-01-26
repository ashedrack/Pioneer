import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List


class ResourceScheduler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scheduled_actions: List[Dict[str, Any]] = []

    async def schedule_action(
        self, resource_id: str, action: str, scheduled_time: datetime
    ) -> Dict[str, Any]:
        """Schedule a resource action (startup/shutdown)."""
        action_id = f"{resource_id}-{action}-{scheduled_time.isoformat()}"

        schedule_entry = {
            "id": action_id,
            "resource_id": resource_id,
            "action": action,
            "scheduled_time": scheduled_time,
            "status": "scheduled",
        }

        self.scheduled_actions.append(schedule_entry)
        self.logger.info(
            f"Scheduled {action} for resource {resource_id} at {scheduled_time}"
        )

        return schedule_entry

    def get_pending_actions(self, window_minutes: int = 30) -> List[Dict[str, Any]]:
        """Get actions scheduled for the next window_minutes."""
        now = datetime.utcnow()
        window_end = now + timedelta(minutes=window_minutes)

        return [
            action
            for action in self.scheduled_actions
            if action["status"] == "scheduled"
            and now <= action["scheduled_time"] <= window_end
        ]

    async def execute_action(self, action: Dict[str, Any]) -> bool:
        """Execute a scheduled action."""
        try:
            # TODO: Implement actual resource management logic
            self.logger.info(
                f"Executing {action['action']} for resource {action['resource_id']}"
            )

            # Simulate action execution
            await asyncio.sleep(2)

            action["status"] = "completed"
            action["execution_time"] = datetime.utcnow()
            return True

        except Exception as e:
            self.logger.error(f"Failed to execute action: {str(e)}")
            action["status"] = "failed"
            action["error"] = str(e)
            return False

    async def run(self) -> None:
        """Main scheduler loop."""
        try:
            while True:
                pending_actions = self.get_pending_actions()

                for action in pending_actions:
                    await self.execute_action(action)

                await asyncio.sleep(60)  # Check every minute

        except Exception as e:
            self.logger.error(f"Scheduler error: {str(e)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scheduler = ResourceScheduler()
    asyncio.run(scheduler.run())
