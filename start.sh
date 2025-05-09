#!/bin/bash

# .env 파일에서 환경 변수 로드
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 기본값 설정
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8501}

# FastAPI 서버를 백그라운드로 실행
uv run python main.py &

# FastAPI 서버가 시작될 때까지 잠시 대기
sleep 3

# Streamlit 앱 실행
uv run streamlit run app.py --server.address $HOST --server.port $PORT

# 스크립트가 종료될 때 FastAPI 서버와 Streamlit 모두 종료
pkill -f "python main.py" || true  # FastAPI 서버 종료 (8000번 포트)
pkill -f "python -m streamlit" || true  # Streamlit 종료