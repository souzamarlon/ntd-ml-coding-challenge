# Use official Python 3.11 slim image with up-to-date SQLite
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install pip and pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock first (for caching)
COPY Pipfile Pipfile.lock ./

# Install dependencies via pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy app code
COPY . .

# Expose default Django port
EXPOSE 8000

# Default command to run the server
ENTRYPOINT ["pipenv", "run"]
