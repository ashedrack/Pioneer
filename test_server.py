from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory storage for users
users_db: Dict[str, dict] = {}

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    company: str
    region: str
    phone: str = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/login")
async def login(user: UserLogin):
    # For testing, accept any credentials
    return {"access_token": "test_token", "token_type": "bearer"}

@app.post("/auth/signup")
async def signup(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[user.email] = user.dict()
    return {"access_token": "test_token", "token_type": "bearer"}

@app.get("/api/v1/resources")
async def get_resources():
    return {
        "status": "success",
        "data": [
            {
                "id": "server-001",
                "name": "Production Web Server",
                "type": "t2.medium",
                "region": "us-west",
                "status": "running"
            },
            {
                "id": "server-002",
                "name": "Database Server",
                "type": "t2.large",
                "region": "us-west",
                "status": "running"
            }
        ]
    }

@app.get("/api/v1/metrics/{resource_id}")
async def get_metrics(resource_id: str):
    return {
        "status": "success",
        "data": {
            "resource_id": resource_id,
            "metrics": [
                {
                    "timestamp": "2025-01-25T00:00:00Z",
                    "metrics": {
                        "cpu_usage": 45.5,
                        "memory_usage": 60.2,
                        "disk_usage": 72.8
                    }
                }
            ]
        }
    }
