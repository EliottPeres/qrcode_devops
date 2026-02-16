# Lightweight base image
FROM python:3.10-slim

# Create a non-root user for security
RUN useradd -m apiuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .

# Change ownership to the non-root user
RUN chown -R apiuser:apiuser /app

# Switch to the secure user
USER apiuser

# HEALTHCHECK: Verifies every 30s that /health endpoint responds correctly
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]