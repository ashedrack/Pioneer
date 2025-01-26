import uuid
from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import models, utils

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# In-memory user storage (replace with database in production)
users_db: Dict[str, dict] = {}


@router.post("/signup", response_model=models.Token)
async def signup(user: models.UserCreate):
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user_dict = user.dict()
    user_dict["id"] = str(uuid.uuid4())
    user_dict["hashed_password"] = utils.get_password_hash(user.password)
    del user_dict["password"]

    users_db[user.email] = user_dict

    access_token = utils.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=models.Token)
async def login(user_credentials: models.UserLogin):
    user = users_db.get(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not utils.verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = utils.create_access_token(
        data={"sub": user_credentials.email},
        expires_delta=timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        email = utils.verify_access_token(token)
        user = users_db.get(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return {
            "email": email,
            "full_name": user["full_name"],
            "company": user["company"],
            "id": user["id"],
            "is_active": True,
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
