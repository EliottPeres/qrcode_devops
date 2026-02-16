import os
import sys
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image as PilImage

def generate():
    # 1. Retrieve the URL passed by the API via environment variables
    url = os.environ.get("URL_TO_GENERATE")

    if not url:
        print("❌ ERROR: No URL provided in 'URL_TO_GENERATE' variable.")
        sys.exit(1)

    # 2. Retrieve customization options (with defaults)
    fill_color = os.environ.get("QR_FILL_COLOR", "#000000")
    back_color = os.environ.get("QR_BACK_COLOR", "#FFFFFF")
    box_size = int(os.environ.get("QR_BOX_SIZE", "10"))
    border = int(os.environ.get("QR_BORDER", "4"))
    error_correction_str = os.environ.get("QR_ERROR_CORRECTION", "M")

    # Map string to qrcode constant
    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    error_correction = ec_map.get(error_correction_str.upper(), qrcode.constants.ERROR_CORRECT_M)

    print(f"⚙️  Generating QR Code for: {url}")
    print(f"   Fill: {fill_color} | Back: {back_color} | Size: {box_size} | Border: {border} | EC: {error_correction_str}")

    # 3. Create the QR Code with customization
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version based on data length
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 4. Generate the image with custom colors
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # 5. Save the image
    output_path = "qrcode.png"
    img.save(output_path)

    print(f"✅ Success! Image saved as: {output_path}")

if __name__ == "__main__":
    generate()