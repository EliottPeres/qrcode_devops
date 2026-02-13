# 📱 Projet DevOps : Générateur de QR Code Distribué

Ce projet est une application microservices permettant de générer des QR Codes à la volée. Il a été conçu pour démontrer la maîtrise des concepts **DevOps** modernes : conteneurisation avancée, orchestration, intégration continue (CI/CD) et sécurité de la chaîne logistique (Supply Chain Security).

---

## 🏗️ Architecture Technique

L'application repose sur une architecture 3-tiers conteneurisée :

1.  **Frontend (Streamlit)** : Interface utilisateur simple pour saisir l'URL à transformer.
2.  **API (FastAPI)** : Chef d'orchestre qui reçoit les demandes et pilote le moteur Docker.
3.  **Worker (Python)** : Conteneur **éphémère** lancé à la demande par l'API pour générer le QR Code (Pattern *Docker-out-of-Docker*).



---

## 🚀 Démarrage Rapide

Le projet est conçu pour être lancé avec une **unique commande**, sans configuration préalable complexe sur l'hôte.

### Prérequis
* Docker Desktop (ou Docker Engine + Compose plugin)

### Lancement
À la racine du projet, exécutez :

```bash
docker compose up --build

```

### Accès

* **Application Web** : [http://localhost:8501](http://localhost:8501)
* **Documentation API (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)
* **Healthcheck** : [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚙️ Points Forts & Choix DevOps

### 1. Orchestration & Docker-out-of-Docker (DooD)

L'API communique directement avec le démon Docker de la machine hôte via le socket `/var/run/docker.sock`. Cela permet à l'API de lancer dynamiquement des conteneurs *workers* pour chaque demande de génération, assurant une isolation totale des tâches.

### 2. Gestion Automatique des Permissions

Pour éviter les erreurs de permissions sur le socket Docker (fréquentes sous Linux/macOS), un service **Init-Container** (`init-permissions`) se lance au démarrage pour configurer les droits nécessaires, puis s'arrête automatiquement. Cela garantit un déploiement fluide sur n'importe quel environnement.

### 3. Sécurité (Security by Design)

* **Utilisateurs Non-Root** : Tous les services (API, Frontend, Worker) s'exécutent avec des utilisateurs dédiés (`apiuser`, `frontuser`, `appuser`) et non en `root`.
* **Images Minimales** : Utilisation d'images `python:3.10-slim` pour réduire la surface d'attaque et la taille des images.
* **Limites de Ressources** : Les workers sont lancés avec des limites de mémoire (`128m`) pour éviter la saturation de l'hôte.

---

## 🔄 Pipeline CI/CD (GitHub Actions)

Le projet intègre un pipeline d'automatisation complet (`.github/workflows/ci-cd.yml`) qui s'exécute à chaque `git push` sur la branche `main`.

### Étapes du Pipeline :

1. **Build** : Construction des images Docker.
2. **Versioning** : Tagging des images avec le SHA du commit Git (Traçabilité).
3. **Scan de Vulnérabilités** : Analyse des images avec **Trivy** pour détecter les failles de sécurité (CVE).
4. **SBOM** : Génération automatique et export du *Software Bill of Materials* (inventaire logiciel) au format CycloneDX.
5. **Déploiement** : Push automatique des images validées sur **Docker Hub**.

---

## 📂 Structure du Projet

```text
.
├── api/                # Backend FastAPI (Orchestrateur)
│   ├── Dockerfile      # Configuration Docker sécurisée (Non-root + Healthcheck)
│   └── main.py         # Logique de l'API et communication Docker
├── frontend/           # Interface Utilisateur Streamlit
│   └── Dockerfile      # Configuration Docker
├── worker/             # Script de génération d'image
│   ├── Dockerfile      # Image légère pour les workers éphémères
│   └── worker.py       # Logique de création du QR Code
├── .github/workflows/  # Configuration CI/CD (Build, Test, Scan, Push)
├── docker-compose.yml  # Orchestration globale de la stack
└── README.md           # Documentation

```

```

```