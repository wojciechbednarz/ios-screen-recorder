# Stage 1: Build the Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# Stage 2: Build the Backend
# Using Python 3.12 for better compatibility
FROM python:3.12-slim AS backend
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy backend source code
COPY src/ ./src/
COPY Procfile .
# --- NEW: Copy these if you need them for initial startup ---
# COPY recordings.db . 
# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
# Create directory for recordings
RUN mkdir -p output/recordings
# Set environment variables
ENV MOCK_MODE=true \
    DATABASE_URL="sqlite:///./recordings.db" \
    PYTHONPATH=. \
    PORT=8000
# Expose the port
EXPOSE 8080
# Start the application using the $PORT variable
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT}"]