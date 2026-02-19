from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import docker
import io
import tarfile
import os

# --- API CONFIGURATION ---
# root_path="/api" is CRUCIAL for Swagger UI to work behind Nginx
app = FastAPI(
    title="QR Code Generator API",
    description="QR Code generation API using Docker workers",
    version="1.0.0",
    root_path="/api"
)

# Connect to host Docker socket
try:
    client = docker.from_env()
except Exception as e:
    print(f"Docker connection error: {e}")
    client = None

# Data model for input validation
class UrlRequest(BaseModel):
    url: str
    fill_color: str = Field(default="#000000", description="QR Code color (hex)")
    back_color: str = Field(default="#FFFFFF", description="Background color (hex)")
    box_size: int = Field(default=10, ge=1, le=50, description="Square size (pixels)")
    border: int = Field(default=4, ge=0, le=20, description="Border thickness")
    error_correction: str = Field(default="M", pattern="^[LMQH]$", description="Error correction: L, M, Q, H")

@app.get("/health")
def health_check():
    """Checks if the API is alive (used by Docker)."""
    if not client:
        return {"status": "error", "detail": "Docker connection failed"}
    return {"status": "ok"}

@app.get("/")
def root():
    """Root route to test connectivity."""
    return {
        "message": "API QR Code Generator is running",
        "docs_url": "/api/docs"
    }

@app.post("/generate")
def generate_qr(request: UrlRequest):
    """
    Launches an ephemeral worker container to generate the QR Code.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Docker daemon not connected")

    container = None
    try:
        print(f"Launching worker for: {request.url}")

        # Worker image name (can be overridden by env variable)
        worker_image = os.getenv("WORKER_IMAGE", "qrcode-worker:1.0.0")

        # 1. Launch Worker container
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
            detach=True,       # Detached mode (background)
            mem_limit="128m",  # Security: RAM limit
            network_disabled=True # Security: Worker doesn't need internet
        )

        # 2. Wait for completion
        result = container.wait()
        
        if result["StatusCode"] != 0:
            raise Exception("Worker failed to generate QR code")

        # 3. Retrieve generated file from container
        # get_archive returns a tuple (stream, stats)
        bits, stat = container.get_archive("/app/qrcode.png")

        # 4. Read data stream in memory
        file_obj = io.BytesIO()
        for chunk in bits:
            file_obj.write(chunk)
        file_obj.seek(0)

        # 5. Extract image from TAR format
        with tarfile.open(fileobj=file_obj) as tar:
            member = tar.getmember("qrcode.png")
            img_data = tar.extractfile(member).read()

        print("Image retrieved successfully")

        # 6. Return image directly (Content-Type: image/png)
        return Response(content=img_data, media_type="image/png")

    except docker.errors.ImageNotFound:
        error_msg = f"Image '{worker_image}' not found. Please build it first."
        print(f"ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 7. CLEANUP: Remove container no matter what
        if container:
            try:
                container.remove(force=True)
                print("Container cleaned up")
            except Exception as e:
                print(f"Failed to remove container: {e}")