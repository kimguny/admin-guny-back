from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.auth import create_access_token, verify_password, hash_password, decode_access_token
from core.database import get_db
from models.user import User
from pydantic import BaseModel

router = APIRouter()

class UserRegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/api/me")
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/login"))):
    payload = decode_access_token(token)
    return {"username": payload["sub"]}

@router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user_data.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user_data.password)

    new_user = User(username=user_data.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "회원가입이 완료되었습니다.", "username": new_user.username}