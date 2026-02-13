# Image de base légère
FROM python:3.10-slim

# Création d'un utilisateur non-root (Sécurité) [cite: 14]
RUN useradd -m apiuser

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY main.py .

# Changement des droits pour l'utilisateur
RUN chown -R apiuser:apiuser /app

# On passe sur l'utilisateur sécurisé
USER apiuser

# HEALTHCHECK (Obligatoire PDF) [cite: 15]
# Vérifie toutes les 30s si /health répond bien
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Lancement de l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]