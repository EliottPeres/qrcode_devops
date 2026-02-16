from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import docker
import io
import tarfile
import os

# --- CONFIGURATION API ---
# root_path="/api" est CRUCIAL pour que Swagger UI fonctionne derrière Nginx
app = FastAPI(
    title="QR Code Generator API",
    description="API de génération de QR Codes via Docker workers",
    version="1.0.0",
    root_path="/api"
)

# Connexion au socket Docker de l'hôte
try:
    client = docker.from_env()
except Exception as e:
    print(f"⚠️ Erreur de connexion Docker: {e}")
    client = None

# Modèle de données pour validation des entrées
class UrlRequest(BaseModel):
    url: str
    fill_color: str = Field(default="#000000", description="Couleur du QR Code (hex)")
    back_color: str = Field(default="#FFFFFF", description="Couleur de fond (hex)")
    box_size: int = Field(default=10, ge=1, le=50, description="Taille des carrés (pixels)")
    border: int = Field(default=4, ge=0, le=20, description="Épaisseur de la bordure")
    error_correction: str = Field(default="M", pattern="^[LMQH]$", description="Correction d'erreur: L, M, Q, H")

@app.get("/health")
def health_check():
    """Vérifie que l'API est en vie (utilisé par Docker)."""
    if not client:
        return {"status": "error", "detail": "Docker connection failed"}
    return {"status": "ok"}

@app.get("/")
def root():
    """Route racine pour tester la connectivité."""
    return {
        "message": "API QR Code Generator is running",
        "docs_url": "/api/docs" # Petit indice pour l'utilisateur
    }

@app.post("/generate")
def generate_qr(request: UrlRequest):
    """
    Lance un conteneur worker éphémère pour générer le QR Code.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Docker daemon not connected")

    container = None
    try:
        print(f"🚀 Launching worker for: {request.url}")

        # Nom de l'image worker (peut être surchargé par variable d'env)
        # Note: Assure-toi que cette image existe localement ou sur le Hub
        worker_image = os.getenv("WORKER_IMAGE", "qrcode-worker:latest")

        # 1. Lancement du conteneur Worker
        container = client.containers.run(
            image=worker_image,
            environment={
                "URL_TO_GENERATE": request.url,
                "QR_FILL_COLOR": request.fill_color,
                "QR_BACK_COLOR": request.back_color,
                "QR_BOX_SIZE": str(request.box_size),
                "QR_BORDER": str(request.border),
                "QR_ERROR_CORRECTION": request.error_correction,
            },
            detach=True,       # Mode détaché (arrière-plan)
            mem_limit="128m",  # Sécurité : Limite de RAM
            network_disabled=True # Sécurité : Le worker n'a pas besoin d'internet
        )

        # 2. Attente de la fin du travail
        result = container.wait()
        
        if result["StatusCode"] != 0:
            raise Exception("Worker failed to generate QR code")

        # 3. Récupération du fichier généré depuis le conteneur
        # get_archive renvoie un tuple (stream, stats)
        bits, stat = container.get_archive("/app/qrcode.png")

        # 4. Lecture du flux de données en mémoire
        file_obj = io.BytesIO()
        for chunk in bits:
            file_obj.write(chunk)
        file_obj.seek(0)

        # 5. Extraction de l'image du format TAR
        with tarfile.open(fileobj=file_obj) as tar:
            member = tar.getmember("qrcode.png")
            img_data = tar.extractfile(member).read()

        print("✅ Image retrieved successfully")

        # 6. Renvoi de l'image directement (Content-Type: image/png)
        return Response(content=img_data, media_type="image/png")

    except docker.errors.ImageNotFound:
        error_msg = f"Image '{worker_image}' not found. Please build it first."
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 7. NETTOYAGE : Suppression du conteneur quoi qu'il arrive
        if container:
            try:
                container.remove(force=True)
                print("🧹 Container cleaned up")
            except Exception as e:
                print(f"⚠️ Failed to remove container: {e}")