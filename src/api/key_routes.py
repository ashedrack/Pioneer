from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .key_management import APIKeyManager

router = APIRouter()
security = HTTPBearer()

# Initialize API Key Manager
key_manager = APIKeyManager(
    {
        "dynamodb_table": "cloud_pioneer_api_keys",
        "secret_key": "your-secret-key",  # In production, use AWS Secrets Manager
    }
)


class APIKeyRequest(BaseModel):
    description: str = ""


class APIKeyResponse(BaseModel):
    api_key: str
    api_key_id: str
    created_at: str


@router.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    request: APIKeyRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """Generate a new API key."""
    try:
        # Get account_id from JWT token
        account_id = "get_account_id_from_token(credentials.credentials)"

        key_details = key_manager.generate_api_key(
            account_id=account_id, description=request.description
        )
        return key_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-keys")
async def list_api_keys(credentials: HTTPAuthorizationCredentials = Security(security)):
    """List all API keys for the account."""
    try:
        # Get account_id from JWT token
        account_id = "get_account_id_from_token(credentials.credentials)"

        keys = key_manager.list_api_keys(account_id)
        return {"api_keys": keys}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api-keys/{api_key_id}")
async def revoke_api_key(
    api_key_id: str, credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Revoke an API key."""
    try:
        # Get account_id from JWT token
        account_id = "get_account_id_from_token(credentials.credentials)"

        success = key_manager.revoke_api_key(account_id, api_key_id)
        if success:
            return {"message": "API key revoked successfully"}
        else:
            raise HTTPException(status_code=404, detail="API key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-keys/validate")
async def validate_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """Validate an API key."""
    try:
        key_details = key_manager.validate_api_key(credentials.credentials)
        if key_details:
            return key_details
        else:
            raise HTTPException(status_code=401, detail="Invalid API key")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
