from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 종속성 주입을 위한 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
