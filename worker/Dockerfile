# Use a lightweight python image
FROM python:3.10-slim

# Create an 'appuser' user to avoid running as root (Security requirement)
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY worker.py .

# IMPORTANT: Change file ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to secure user
USER appuser

# Launch command
CMD ["python", "worker.py"]