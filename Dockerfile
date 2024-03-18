# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.13
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

from base AS airhouse-migrate
COPY . .
RUN python -m pip install -r requirements.txt

FROM base AS airhouse-test
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

FROM base AS airhouse-app
COPY . .
RUN python -m pip install -r requirements.txt

EXPOSE 8000
