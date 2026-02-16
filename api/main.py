from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import docker
import io
import tarfile
import os

app = FastAPI()
client = docker.from_env()  # Connect to local Docker daemon


class UrlRequest(BaseModel):
    url: str
    fill_color: str = Field(default="#000000", description="QR code foreground color (hex)")
    back_color: str = Field(default="#FFFFFF", description="QR code background color (hex)")
    box_size: int = Field(default=10, ge=1, le=50, description="Size of each QR box in pixels")
    border: int = Field(default=4, ge=0, le=20, description="Border thickness in boxes")
    error_correction: str = Field(default="M", pattern="^[LMQH]$", description="Error correction level: L, M, Q, H")


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
        print(f"Options: fill={request.fill_color}, back={request.back_color}, "
              f"size={request.box_size}, border={request.border}, ec={request.error_correction}")

        # 1. Launch the Worker container with all customization env vars
        container = client.containers.run(
            image="qrcode-worker:latest",
            environment={
                "URL_TO_GENERATE": request.url,
                "QR_FILL_COLOR": request.fill_color,
                "QR_BACK_COLOR": request.back_color,
                "QR_BOX_SIZE": str(request.box_size),
                "QR_BORDER": str(request.border),
                "QR_ERROR_CORRECTION": request.error_correction,
            },
            detach=True,       # Run in background
            mem_limit="128m"   # Security: limit memory usage
        )

        # 2. Wait for container to finish (exit code 0)
        container.wait()

        # 3. Retrieve 'qrcode.png' file from '/app' directory in the container
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