# On utilise une image python légère
FROM python:3.10-slim

# On crée un utilisateur 'appuser' pour ne pas être root (Sécurité PDF)
RUN useradd -m appuser

# On définit le dossier de travail
WORKDIR /app

# On installe les dépendances en tant que root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le code
COPY worker.py .

# IMPORTANT : On change le propriétaire des fichiers pour l'utilisateur non-root
RUN chown -R appuser:appuser /app

# On passe sur l'utilisateur sécurisé
USER appuser

# Commande de lancement
CMD ["python", "worker.py"]