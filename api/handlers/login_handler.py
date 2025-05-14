from core.auth import create_access_token, verify_password, hash_password, decode_access_token
from sqlalchemy.future import select
from models.user import User
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

async def login(form_data, db: AsyncSession):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def register(user_data, db: AsyncSession):
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

def get_current_user(token: str):
    payload = decode_access_token(token)
    return {"username": payload["sub"]}
