import os
import sys
import qrcode

def generate():
    # 1. Retrieve the URL passed by the API via environment variables
    url = os.environ.get("URL_TO_GENERATE")

    if not url:
        print("❌ ERROR: No URL provided in 'URL_TO_GENERATE' variable.")
        sys.exit(1)

    print(f"⚙️  Generating QR Code for: {url}")

    # 2. Create the QR Code image
    img = qrcode.make(url)
    
    # 3. Save (for now, save next to the script)
    output_path = "qrcode.png"
    img.save(output_path)
    
    print(f"✅ Success! Image saved as: {output_path}")

if __name__ == "__main__":
    generate()