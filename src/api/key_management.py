import base64
import hashlib
import hmac
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import boto3


class APIKeyManager:
    def __init__(self, config: Dict):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(config["dynamodb_table"])
        self.secret_key = config["secret_key"]

    def generate_api_key(self, account_id: str, description: str = "") -> Dict:
        """Generate a new API key for an account."""
        # Generate a unique key
        key_uuid = str(uuid.uuid4())
        timestamp = str(int(datetime.utcnow().timestamp()))

        # Create the API key using HMAC
        message = f"{account_id}:{key_uuid}:{timestamp}".encode()
        hmac_obj = hmac.new(self.secret_key.encode(), message, hashlib.sha256)
        api_key = f"cp_{base64.urlsafe_b64encode(hmac_obj.digest()).decode()}"

        # Store the key details
        key_item = {
            "account_id": account_id,
            "api_key_id": key_uuid,
            "api_key_hash": hashlib.sha256(api_key.encode()).hexdigest(),
            "description": description,
            "created_at": timestamp,
            "status": "active",
            "last_used": timestamp,
        }

        self.table.put_item(Item=key_item)

        return {
            "api_key": api_key,
            "api_key_id": key_uuid,
            "created_at": datetime.fromtimestamp(int(timestamp)).isoformat(),
        }

    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate an API key and return account details if valid."""
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Scan for the key (in production, use a GSI for better performance)
        response = self.table.scan(
            FilterExpression="api_key_hash = :hash AND status = :status",
            ExpressionAttributeValues={":hash": key_hash, ":status": "active"},
        )

        if response["Items"]:
            key_details = response["Items"][0]

            # Update last used timestamp
            self.table.update_item(
                Key={
                    "account_id": key_details["account_id"],
                    "api_key_id": key_details["api_key_id"],
                },
                UpdateExpression="SET last_used = :timestamp",
                ExpressionAttributeValues={
                    ":timestamp": str(int(datetime.utcnow().timestamp()))
                },
            )

            return {
                "account_id": key_details["account_id"],
                "api_key_id": key_details["api_key_id"],
                "created_at": datetime.fromtimestamp(
                    int(key_details["created_at"])
                ).isoformat(),
            }

        return None

    def revoke_api_key(self, account_id: str, api_key_id: str) -> bool:
        """Revoke an API key."""
        try:
            self.table.update_item(
                Key={"account_id": account_id, "api_key_id": api_key_id},
                UpdateExpression="SET status = :status",
                ExpressionAttributeValues={":status": "revoked"},
            )
            return True
        except Exception:
            return False

    def list_api_keys(self, account_id: str) -> List[Dict]:
        """List all API keys for an account."""
        response = self.table.query(
            KeyConditionExpression="account_id = :account_id",
            ExpressionAttributeValues={":account_id": account_id},
        )

        return [
            {
                "api_key_id": item["api_key_id"],
                "description": item["description"],
                "created_at": datetime.fromtimestamp(
                    int(item["created_at"])
                ).isoformat(),
                "status": item["status"],
                "last_used": datetime.fromtimestamp(int(item["last_used"])).isoformat(),
            }
            for item in response["Items"]
        ]
