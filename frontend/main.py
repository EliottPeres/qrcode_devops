import streamlit as st
import requests
from PIL import Image
import io
import os

st.title("Générateur de QR Code DevOps")

url_input = st.text_input("URL à transformer", "https://google.com")

# URL de l'API
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if st.button("Générer"):
    if url_input:
        with st.spinner('Le worker fabrique votre QR Code...'):
            try:
                # On envoie la demande
                response = requests.post(API_URL, json={"url": url_input})
                
                # Si ça marche (200 OK)
                if response.status_code == 200:
                    # C'EST ICI QUE CA CHANGE :
                    # On ne fait pas response.json(), mais on lit le contenu binaire (content)
                    image_data = response.content
                    
                    # On transforme les octets en Image affichable
                    image = Image.open(io.BytesIO(image_data))
                    
                    st.success("QR Code reçu avec succès !")
                    st.image(image, caption=f"QR Code vers {url_input}")
                
                else:
                    st.error(f"Erreur API ({response.status_code}) : {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Impossible de contacter l'API. Vérifiez qu'elle tourne sur le port 8000.")
            except Exception as e:
                st.error(f"Erreur technique : {e}")
    else:
        st.warning("Veuillez entrer une URL.")