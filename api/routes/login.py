from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from pydantic import BaseModel
from api.handlers import login_handler

router = APIRouter()

class UserRegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_handler.login(form_data, db)

@router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    return await login_handler.register(user_data, db)

@router.get("/api/me")
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/login"))):
    return login_handler.get_current_user(token)
