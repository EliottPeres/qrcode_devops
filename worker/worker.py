import os
import sys
import qrcode

def generate():
    # 1. On récupère l'URL transmise par l'API via les variables d'environnement
    url = os.environ.get("URL_TO_GENERATE")

    if not url:
        print("❌ ERREUR : Aucune URL fournie dans la variable 'URL_TO_GENERATE'.")
        sys.exit(1)

    print(f"⚙️  Génération du QR Code pour : {url}")

    # 2. Création de l'image QR Code
    img = qrcode.make(url)
    
    # 3. Sauvegarde (pour l'instant, on sauvegarde juste à côté du script)
    output_path = "qrcode.png"
    img.save(output_path)
    
    print(f"✅ Succès ! Image sauvegardée sous : {output_path}")

if __name__ == "__main__":
    generate()