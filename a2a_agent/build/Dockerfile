FROM python:3.12-slim-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install -U pip && pip install uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-install-project

# Copy source code
COPY src ./src

# Install the project itself
RUN uv pip install .

EXPOSE 10000