from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import login
from core.database import engine
from models.user import Base

# Lifespan 이벤트 핸들러 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # 서버가 실행될 때만 실행되고 종료 시 정리할 작업 가능

app = FastAPI(lifespan=lifespan)

# 라우터 등록
app.include_router(login.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with PostgreSQL!"}
