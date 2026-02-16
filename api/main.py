from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import docker
import io
import tarfile
import os

app = FastAPI()
client = docker.from_env()  # Connect to local Docker daemon

class UrlRequest(BaseModel):
    url: str

@app.get("/health")
def health_check():
    # Allows Docker to verify that the API is alive
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API QR Code Generator is running"}

@app.post("/generate")
def generate_qr(request: UrlRequest):
    container = None
    try:
        print(f"Launching worker for: {request.url}")
        
        # 1. Launch the Worker container
        # Pass the URL via environment variable as defined in worker.py
        container = client.containers.run(
            image="qrcode-worker:latest",
            environment={"URL_TO_GENERATE": request.url},
            detach=True,       # Run in background
            mem_limit="128m"   # Security: limit memory usage (best practice)
        )
        
        # 2. Wait for container to finish (exit code 0)
        container.wait()
        
        # 3. Retrieve 'qrcode.png' file from '/app' directory in the container
        # Docker returns a TAR stream (archive), not the direct file
        bits, stat = container.get_archive("/app/qrcode.png")
        
        # 4. Read the stream into memory
        file_obj = io.BytesIO()
        for chunk in bits:
            file_obj.write(chunk)
        file_obj.seek(0)
        
        # 5. Extract the image from the TAR archive
        with tarfile.open(fileobj=file_obj) as tar:
            member = tar.getmember("qrcode.png")
            img_data = tar.extractfile(member).read()
            
        print("Image retrieved successfully")
        
        # 6. Return the image directly to frontend (PNG format)
        return Response(content=img_data, media_type="image/png")

    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=500, detail="Image 'qrcode-worker' not found. Did you run the build?")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 7. CLEANUP: Always remove the container, even on error
        if container:
            try:
                container.remove(force=True)
                print("Container cleaned up")
            except:
                pass