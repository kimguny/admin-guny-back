from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# 로그인 요청 모델
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
def login(request: LoginRequest):
    # 간단한 인증 로직 (실제 서비스에서는 DB 검증 필요)
    if request.username == "admin" and request.password == "password":
        return {"message": "Login successful", "token": "fake-jwt-token"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
