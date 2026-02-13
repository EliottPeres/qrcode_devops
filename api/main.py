from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import docker
import io
import tarfile
import os

app = FastAPI()
client = docker.from_env() # Connexion au Docker local

class UrlRequest(BaseModel):
    url: str

@app.get("/health")
def health_check():
    # Permet à Docker de vérifier que l'API est en vie
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API QR Code Generator is running"}

@app.post("/generate")
def generate_qr(request: UrlRequest):
    container = None
    try:
        print(f"🔨 Lancement du worker pour : {request.url}")
        
        # 1. Lancer le conteneur Worker
        # On lui passe l'URL via la variable d'environnement définie dans le worker.py
        container = client.containers.run(
            image="qrcode-worker:latest",
            environment={"URL_TO_GENERATE": request.url},
            detach=True,       # On le lance en arrière-plan
            mem_limit="128m"   # Sécurité : on limite la mémoire (Bonne pratique)
        )
        
        # 2. Attendre qu'il finisse (exit code 0)
        container.wait()
        
        # 3. Récupérer le fichier 'qrcode.png' depuis le dossier '/app' du conteneur
        # Docker renvoie un flux TAR (archive), pas le fichier direct
        bits, stat = container.get_archive("/app/qrcode.png")
        
        # 4. Lire le flux en mémoire
        file_obj = io.BytesIO()
        for chunk in bits:
            file_obj.write(chunk)
        file_obj.seek(0)
        
        # 5. Extraire l'image du TAR
        with tarfile.open(fileobj=file_obj) as tar:
            member = tar.getmember("qrcode.png")
            img_data = tar.extractfile(member).read()
            
        print("✅ Image récupérée avec succès !")
        
        # 6. Renvoyer l'image directement au front (format PNG)
        return Response(content=img_data, media_type="image/png")

    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=500, detail="L'image 'qrcode-worker' est introuvable. Avez-vous fait le build ?")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 7. NETTOYAGE : Toujours supprimer le conteneur, même en cas d'erreur
        if container:
            try:
                container.remove(force=True)
                print("🧹 Conteneur nettoyé.")
            except:
                pass