# Python 3.12 공식 이미지 사용
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정 (Python이 .pyc 파일을 생성하지 않도록 설정)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# pip 최신화 및 의존성 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 서버 실행 (기본적으로 uvicorn 실행)
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]