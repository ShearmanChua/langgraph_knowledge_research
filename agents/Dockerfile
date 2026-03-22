FROM python:3.12-slim-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

RUN apt update && apt upgrade -y 
RUN apt-get upgrade -y
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        perl \
        pkg-config \
        libclang-dev \
        musl-tools \
        git && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./
# Install uv for fast package management
RUN pip install --upgrade pip uv playwright

# Install dependencies (without project yet)
RUN uv sync --no-install-project

# Copy source code
COPY src ./src

# Install the project itself
RUN uv pip install .

RUN playwright install

RUN playwright install-deps
