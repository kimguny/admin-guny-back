from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.auth import create_access_token, verify_password, hash_password
from core.database import get_db
from models.user import User

router = APIRouter()

@router.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/api/me")
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/login"))):
    from core.auth import decode_access_token
    payload = decode_access_token(token)
    return {"username": payload["sub"]}

@router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register(username: str, password: str, db: Session = Depends(get_db)):
    # 사용자 중복 확인
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(password)

    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "회원가입이 완료되었습니다.", "username": new_user.username}