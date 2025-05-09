FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked
RUN chmod +x /app/start.sh


CMD ["/app/start.sh"]