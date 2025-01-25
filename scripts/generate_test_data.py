"""Script to generate and submit test metrics data."""
import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000/api/v1"

def generate_metrics(start_time: datetime, num_points: int = 24) -> list:
    """Generate dummy metrics data for testing."""
    data_points = []
    for i in range(num_points):
        timestamp = start_time + timedelta(hours=i)
        metrics = {
            "resource_id": "test-instance-1",
            "timestamp": timestamp.isoformat(),
            "metrics": {
                "cpu_usage": random.uniform(20, 95),
                "memory_usage": random.uniform(30, 85),
                "disk_usage": random.uniform(40, 75),
                "network_in": random.uniform(100, 1000),
                "network_out": random.uniform(100, 1000)
            }
        }
        data_points.append(metrics)
    return data_points

def submit_metrics(metrics_data: list) -> None:
    """Submit metrics to the API."""
    for metrics in metrics_data:
        response = requests.post(f"{BASE_URL}/metrics", json=metrics)
        print(f"Submitted metrics for {metrics['timestamp']}: {response.json()}")

def schedule_actions() -> None:
    """Schedule some test actions."""
    actions = [
        {
            "resource_id": "test-instance-1",
            "action": "stop",
            "scheduled_time": (datetime.now() + timedelta(hours=6)).isoformat()
        },
        {
            "resource_id": "test-instance-1",
            "action": "start",
            "scheduled_time": (datetime.now() + timedelta(hours=12)).isoformat()
        }
    ]
    
    for action in actions:
        response = requests.post(f"{BASE_URL}/schedule", json=action)
        print(f"Scheduled {action['action']}: {response.json()}")

def main():
    """Main function to generate and submit test data."""
    print("Generating and submitting test metrics...")
    start_time = datetime.now() - timedelta(days=1)  # Start from 24 hours ago
    metrics_data = generate_metrics(start_time)
    submit_metrics(metrics_data)
    
    print("\nScheduling test actions...")
    schedule_actions()
    
    print("\nChecking scheduled actions...")
    response = requests.get(f"{BASE_URL}/schedule/test-instance-1")
    print(f"Scheduled actions: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    main()
