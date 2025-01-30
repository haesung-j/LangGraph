# 기본 이미지 설정
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 및 캐시 정리
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 애플리케이션 파일을 컨테이너에 복사
COPY . /app/

# requirements.txt 파일을 컨테이너에 복사하고 패키지 설치
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 환경 변수 설정
ENV PORT=8000
ENV HOST=0.0.0.0

# FastAPI와 Streamlit 포트 노출
EXPOSE 8000
EXPOSE 8501

# 시작 스크립트 생성
RUN echo '#!/bin/bash\n\
uvicorn main:app --host $HOST --port $PORT & \n\
streamlit run app.py --server.port 8501 --server.address $HOST\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# 컨테이너 실행 시 시작 스크립트 실행
CMD ["/app/start.sh"]