import streamlit as st
import requests
from PIL import Image
import io
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="QR Gen - DevOps",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS STYLING
st.markdown("""
    <style>
    /* Global application background */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Titles */
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
    
    /* Button styling */
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

    /* Specific styling for text input field */
    .stTextInput input {
        background-color: #ffffff !important;  /* WHITE background for input */
        color: #333333 !important;             /* Dark grey text */
        border: 2px solid #e0e0e0 !important;  /* Light border */
        border-radius: 8px !important;         /* Rounded corners */
    }
    
    /* Border color change on focus */
    .stTextInput input:focus {
        border-color: #FF4B4B !important;
        box-shadow: 0 0 5px rgba(255, 75, 75, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png", width=100)
    st.title("About")
    st.info(
        """
        This project is a complete **DevOps** demonstration.
        
        **Technologies:**
        * 🐳 Docker & Compose
        * 🐍 FastAPI & Python
        * 🎨 Streamlit
        * 🚀 GitHub Actions
        """
    )
    st.markdown("---")
    st.write("© 2026 - M2 Project")

# 4. MAIN CONTENT
st.markdown('<div class="main-title">QR Code Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transform your URLs into images instantly via our microservices architecture.</div>', unsafe_allow_html=True)

# Input area
with st.container():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # Input field with white background
        url_input = st.text_input("Paste your URL here:", "https://youtube.com")
        
        generate_btn = st.button("🚀 Generate QR Code")

# API logic
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if generate_btn:
    if url_input:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.spinner('🏗️ Docker worker is building your image...'):
                try:
                    response = requests.post(API_URL, json={"url": url_input})
                    
                    if response.status_code == 200:
                        image_data = response.content
                        image = Image.open(io.BytesIO(image_data))
                        
                        st.success("✅ QR Code generated successfully!")
                        
                        st.image(image, use_container_width=True)
                        
                        st.download_button(
                            label="📥 Download image",
                            data=image_data,
                            file_name="qrcode.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"🚨 Unable to contact API. Please check Docker.")
    else:
        st.warning("⚠️ Please enter a valid URL.")