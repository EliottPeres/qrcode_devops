import streamlit as st
import requests
from PIL import Image
import io
import os

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="QR Gen - DevOps",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. STYLE CSS PERSONNALISÉ (C'est ici que ça change)
st.markdown("""
    <style>
    /* Fond global de l'application */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Titres */
    .main-title {
        font-size: 3rem;
        color: #4B4B4B;
        text-align: center;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Style du bouton */
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        color: white;
    }

    /* --- NOUVEAU : Style spécifique pour le champ de texte (Input) --- */
    .stTextInput input {
        background-color: #ffffff !important;  /* Fond BLANC pour l'input */
        color: #333333 !important;             /* Texte gris foncé */
        border: 2px solid #e0e0e0 !important;  /* Bordure légère */
        border-radius: 8px !important;         /* Coins arrondis */
    }
    
    /* Changement de couleur de la bordure quand on clique dedans (Focus) */
    .stTextInput input:focus {
        border-color: #FF4B4B !important;
        box-shadow: 0 0 5px rgba(255, 75, 75, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png", width=100)
    st.title("À propos")
    st.info(
        """
        Ce projet est une démonstration **DevOps** complète.
        
        **Technologies :**
        * 🐳 Docker & Compose
        * 🐍 FastAPI & Python
        * 🎨 Streamlit
        * 🚀 GitHub Actions
        """
    )
    st.markdown("---")
    st.write("© 2026 - Projet M2")

# 4. CONTENU PRINCIPAL
st.markdown('<div class="main-title">Générateur QR Code</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transformez vos URLs en images instantanément via notre architecture microservices.</div>', unsafe_allow_html=True)

# Zone de saisie
with st.container():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # Le champ qui aura maintenant un fond blanc
        url_input = st.text_input("Collez votre URL ici :", "https://youtube.com")
        
        generate_btn = st.button("🚀 Générer mon QR Code")

# Logique de l'API
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if generate_btn:
    if url_input:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.spinner('🏗️ Le worker Docker construit votre image...'):
                try:
                    response = requests.post(API_URL, json={"url": url_input})
                    
                    if response.status_code == 200:
                        image_data = response.content
                        image = Image.open(io.BytesIO(image_data))
                        
                        st.success("✅ QR Code généré avec succès !")
                        
                        st.image(image, use_container_width=True)
                        
                        st.download_button(
                            label="📥 Télécharger l'image",
                            data=image_data,
                            file_name="qrcode.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error(f"❌ Erreur API : {response.status_code}")
                        
                except Exception as e:
                    st.error(f"🚨 Impossible de contacter l'API. Vérifiez Docker.")
    else:
        st.warning("⚠️ Veuillez entrer une URL valide.")