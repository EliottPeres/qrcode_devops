FROM python:3.10-slim

# Utilisateur non-root [cite: 14]
RUN useradd -m frontuser

WORKDIR /app

COPY requirements.txt .
# Ajout de curl pour les tests réseaux si besoin
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN chown -R frontuser:frontuser /app

USER frontuser

# Streamlit tourne sur le port 8501 par défaut
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]