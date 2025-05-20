# syntax=docker/dockerfile:1.4

FROM python:3.11-slim

ARG AUTHOR="karmichael228"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AUTHOR=$AUTHOR

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r echouser && useradd -r -g echouser echouser

WORKDIR /app

COPY main.py .

RUN python --version

RUN chown -R echouser:echouser /app

USER echouser

EXPOSE 8000

CMD ["python", "main.py"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD sleep 5 && curl -f http://localhost:8000 || exit 1 