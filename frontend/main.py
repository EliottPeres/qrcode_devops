import streamlit as st
import requests
from PIL import Image
import io
import os
import time

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="QR Gen — DevOps Studio",
    page_icon="◻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. MINIMAL CSS - ONLY ESSENTIALS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header, [data-testid="stHeader"], 
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Hide sidebar */
    section[data-testid="stSidebar"], 
    button[kind="header"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Global styling */
    .stApp {
        background: #F8FAFC !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .block-container {
        max-width: 720px !important;
        padding: 3rem 1rem 2rem 1rem !important;
    }
    
    /* Form inputs */
    .stTextInput input, .stSelectbox select {
        border-radius: 12px !important;
        border: 1.5px solid #E5E7EB !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.08) !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: #111827 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 52px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #1F2937 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(17, 24, 39, 0.3) !important;
    }
    
    .stDownloadButton > button {
        border-radius: 12px !important;
        border: 1.5px solid #E5E7EB !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: #111827 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Status messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 12px !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: #111827 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. HEADER - PURE MARKDOWN
# ─────────────────────────────────────────────
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
            <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #111827, #374151); 
                        border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                        color: white; font-weight: 900; font-size: 1.1rem;">Q</div>
            <span style="font-size: 1.3rem; font-weight: 800; color: #111827;">QR Gen</span>
            <span style="font-size: 0.6rem; font-weight: 700; color: #6B7280; 
                         background: rgba(107, 114, 128, 0.1); padding: 3px 10px; 
                         border-radius: 100px; letter-spacing: 1px;">DEVOPS</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 1.5rem;">
            <div style="width: 7px; height: 7px; border-radius: 50%; background: #10B981;"></div>
            <span style="font-size: 0.75rem; font-weight: 600; color: #6B7280;">All systems operational</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("# Generate a QR Code.")
st.markdown("##### Paste a URL, customize the output, and download a production-ready QR image.")
st.markdown("---")


# ─────────────────────────────────────────────
# 4. INPUT SECTION - MARKDOWN HEADERS
# ─────────────────────────────────────────────
st.markdown("###  Target URL")
url_input = st.text_input(
    "URL", 
    "https://youtube.com",
    label_visibility="collapsed",
    placeholder="https://example.com"
)

st.markdown("---")

# ─────────────────────────────────────────────
# 5. DESIGN SECTION
# ─────────────────────────────────────────────
st.markdown("###  Appearance")

col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("**Foreground**", "#111827")
with col2:
    back_color = st.color_picker("**Background**", "#FFFFFF")

st.markdown("")
box_size = st.slider("**Module size (px)**", min_value=1, max_value=50, value=10)
border = st.slider("**Quiet zone (modules)**", min_value=0, max_value=20, value=4)

st.markdown("---")


# ─────────────────────────────────────────────
# 6. ERROR CORRECTION - MARKDOWN TABLE
# ─────────────────────────────────────────────
st.markdown("###  Error Correction")

error_correction = st.selectbox(
    "Level",
    options=["L", "M", "Q", "H"],
    index=1,
    label_visibility="collapsed"
)

st.markdown("""
| Level | Recovery Rate |
|:-----:|:-------------:|
| **L** | 7% Recovery   |
| **M** | 15% Recovery  |
| **Q** | 25% Recovery  |
| **H** | 30% Recovery  |
""")

st.markdown("")


# ─────────────────────────────────────────────
# 7. GENERATE BUTTON
# ─────────────────────────────────────────────
generate_btn = st.button("🚀 GENERATE QR CODE")


# ─────────────────────────────────────────────
# 8. API CALL & RESULT
# ─────────────────────────────────────────────
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if generate_btn:
    if url_input:
        with st.spinner("⚡ Generating via worker container..."):
            try:
                payload = {
                    "url": url_input,
                    "fill_color": fill_color,
                    "back_color": back_color,
                    "box_size": box_size,
                    "border": border,
                    "error_correction": error_correction,
                }

                start_time = time.time()
                response = requests.post(API_URL, json=payload)
                elapsed = round(time.time() - start_time, 2)

                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))

                    st.success(f"✅ Generated in {elapsed}s")
                    
                    st.markdown("---")
                    st.markdown("###  Your QR Code")

                    col_qr, col_info = st.columns([1, 1])

                    with col_qr:
                        st.image(image, use_container_width=True)

                    with col_info:
                        st.markdown(f"""
                        **Configuration Details:**
                        
                        - **URL:** `{url_input[:40]}{'...' if len(url_input) > 40 else ''}`
                        - **Colors:** `{fill_color}` / `{back_color}`
                        - **Module:** `{box_size}px`
                        - **Border:** `{border} modules`
                        - **EC Level:** `{error_correction}`
                        - **Latency:** `{elapsed}s`
                        """)
                        
                        st.markdown("")
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_data,
                            file_name="qrcode.png",
                            mime="image/png",
                            use_container_width=True
                        )

                else:
                    st.error(f"❌ API returned status {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot reach the API. Ensure Docker containers are running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid URL.")


# ─────────────────────────────────────────────
# 9. FOOTER - MARKDOWN
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
    <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem;">
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">Docker</span>
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">FastAPI</span>
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">Streamlit</span>
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">GitHub Actions</span>
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">Trivy</span>
        <span style="font-size: 0.7rem; font-weight: 600; color: #9CA3AF; 
                     background: rgba(156, 163, 175, 0.08); padding: 4px 12px; 
                     border-radius: 100px; border: 1px solid rgba(156, 163, 175, 0.12);">CycloneDX</span>
    </div>
    <div style="font-size: 0.7rem; color: #C4C9D4; font-weight: 500;">
        JUNIA 2026 — M2 Project · V. Damery · H. Many · E. Peres
    </div>
</div>
""", unsafe_allow_html=True)