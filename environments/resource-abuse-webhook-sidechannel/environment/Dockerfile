FROM python:3.11.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN chmod +x /app/sync.py

ENV PYTHONUNBUFFERED=1
