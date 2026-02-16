FROM python:3.10-slim

# Create non-root user for security
RUN useradd -m frontuser

WORKDIR /app

COPY requirements.txt .
# Install curl for network health checks if needed
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN chown -R frontuser:frontuser /app

USER frontuser

# Streamlit runs on port 8501 by default
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]