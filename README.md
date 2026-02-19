# Projet DevOps: Distributed QR Code Generator

This project is a microservices application for generating QR Codes on-demand. It demonstrates modern DevOps concepts: advanced containerization, orchestration, continuous integration (CI/CD), and supply chain security.

---

## Technical Architecture

The application is built on a containerized 3-tier architecture:

1. **Frontend (Streamlit)**: Simple user interface for entering URLs to transform.
2. **API (FastAPI)**: Orchestrator that receives requests and controls the Docker engine.
3. **Worker (Python)**: Ephemeral container launched on-demand by the API to generate QR Codes (Docker-out-of-Docker pattern).

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                            │
│                  (http://localhost)                         │
└────────────────────────────────┬────────────────────────────┘
                                 │
                                 ▼
         ┌──────────────────────────────────────────┐
         │           Nginx Reverse Proxy            │
         │         (Port 80 / Gateway)              │
         └──────────────┬──────────────┬────────────┘
                        │              │
            ┌───────────▼─┐        ┌───▼────────────┐
            │  Frontend   │        │      API       │
            │ (Streamlit) │        │   (FastAPI)    │
            │  Port 8501  │        │   Port 8000    │
            └─────────────┘        └────────┬───────┘
                                           │
                          ┌────────────────▼────────────────┐
                          │   Docker Daemon (Host)          │
                          │   /var/run/docker.sock          │
                          └────────────────┬────────────────┘
                                           │
                                           │ (launches on-demand)
                                           ▼
                          ┌────────────────────────────────┐
                          │   Worker Container (QR Gen)    │
                          │   (Ephemeral - runs once)      │
                          │   Memory limit: 128MB           │
                          └────────────────────────────────┘
```

---

## Quick Start

The project is designed to launch with a single command, without complex host configuration.

### Prerequisites
* Docker Desktop (or Docker Engine + Compose plugin)

### Launch
From the project root, execute:

```bash
docker compose up --build
```

### Access

* **Web Application**: [http://localhost](http://localhost)
* **API Documentation (Swagger)**: [http://localhost/api/docs](http://localhost/api/docs)
* **Healthcheck**: [http://localhost/api/health](http://localhost/api/health)

---

## Key Features & DevOps Choices

### 1. Reverse Proxy with Nginx

The project uses **Nginx** as a reverse proxy gateway (port 80) to route requests to the appropriate services:
- Requests to `/` are forwarded to the **Frontend** (Streamlit)
- Requests to `/api` are forwarded to the **API** (FastAPI)

This provides a single entry point for users, unifies the application under one domain, and allows for advanced routing, caching, and security policies.

### 2. Orchestration & Docker-out-of-Docker (DooD)

The API communicates directly with the host machine's Docker daemon via the `/var/run/docker.sock` socket. This allows the API to dynamically launch worker containers for each generation request, ensuring complete task isolation.

### 3. Automatic Permission Management

To avoid permission errors on the Docker socket (common on Linux/macOS), an Init-Container service (`init-permissions`) launches at startup to configure necessary rights, then automatically stops. This ensures smooth deployment on any environment.

### 4. Security (Security by Design)

* **Non-Root Users**: All services (API, Frontend, Worker) run with dedicated users (`apiuser`, `frontuser`, `appuser`) instead of `root`.
* **Minimal Images**: Uses `python:3.10-slim` images to reduce attack surface and image size.
* **Resource Limits**: Workers are launched with memory limits (`128m`) to prevent host saturation.

---

## CI/CD Pipeline (GitHub Actions)

The project includes a complete automation pipeline (`.github/workflows/ci-cd.yml`) that runs on every `git push` to the `main` branch.

### Pipeline Stages:

1. **Build**: Docker image construction.
2. **Versioning**: Image tagging with Git commit SHA (Traceability).
3. **Vulnerability Scanning**: Image analysis with **Trivy** to detect security flaws (CVE).
4. **SBOM**: Automatic generation and export of Software Bill of Materials (software inventory) in CycloneDX format.
5. **Deployment**: Automatic push of validated images to **Docker Hub**.

---

## Project Structure

```text
qrcode_projet/
├── .github/
│   └── workflows/
│       └── ci_cd.yml           # CI/CD pipeline configuration
├── api/                         # FastAPI Backend (Orchestrator)
│   ├── __pycache__/             # Python cache
│   ├── Dockerfile               # Secure Docker configuration
│   ├── main.py                  # API logic and Docker communication
│   └── requirements.txt          # Python dependencies
├── frontend/                     # Streamlit User Interface
│   ├── Dockerfile               # Docker configuration
│   ├── main.py                  # Streamlit app
│   └── requirements.txt          # Python dependencies
├── nginx/                        # Reverse Proxy Gateway
│   └── nginx.conf               # Nginx routing configuration
├── worker/                       # QR Code Generator (Ephemeral)
│   ├── Dockerfile               # Lightweight image for worker
│   ├── requirements.txt          # Python dependencies
│   └── worker.py                # QR Code generation logic
├── .env                          # Environment configuration (optional)
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Services orchestration
├── qrcode.png                    # Generated QR code example
└── README.md                     # Documentation (this file)
```
