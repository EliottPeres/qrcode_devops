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
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 2026 APPLE-INSPIRED DESIGN SYSTEM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ==================== GLOBAL ==================== */
    .stApp {
        background-color: #F5F5F7 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remove default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px !important;
    }

    /* ==================== SIDEBAR — FROSTED ACRYLIC ==================== */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(40px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #1D1D1F !important;
    }

    /* ==================== TYPOGRAPHY ==================== */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: #1D1D1F;
        line-height: 1.05;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 400;
        color: #86868B;
        letter-spacing: -0.2px;
        line-height: 1.5;
        margin-bottom: 32px;
    }
    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #86868B;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1D1D1F;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }

    /* ==================== BENTO CARDS ==================== */
    .bento-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .bento-card:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06), 0 8px 24px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }

    /* Result card — larger emphasis */
    .bento-card-result {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 24px;
        padding: 36px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 8px 32px rgba(0, 0, 0, 0.06);
        animation: resultReveal 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    @keyframes resultReveal {
        0% { opacity: 0; transform: translateY(16px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* ==================== FORM INPUTS ==================== */
    .stTextInput > div > div > input {
        background: #F5F5F7 !important;
        color: #1D1D1F !important;
        border: 1.5px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.25s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #C6F135 !important;
        box-shadow: 0 0 0 3px rgba(198, 241, 53, 0.2) !important;
        background: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #AEAEB2 !important;
    }

    /* Labels */
    .stTextInput label, .stSlider label, .stSelectbox label, .stColorPicker label,
    div[data-testid="stWidgetLabel"] label {
        color: #1D1D1F !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: -0.1px !important;
    }

    /* Slider track */
    .stSlider > div > div > div > div {
        background: #C6F135 !important;
    }
    .stSlider > div > div > div {
        background: rgba(0, 0, 0, 0.06) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #F5F5F7 !important;
        border: 1.5px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 14px !important;
        color: #1D1D1F !important;
    }

    /* ==================== CTA BUTTON — CYBER LIME ==================== */
    .stButton > button {
        width: 100%;
        background: #C6F135 !important;
        color: #1D1D1F !important;
        border: none !important;
        border-radius: 16px !important;
        height: 56px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        box-shadow: 0 2px 8px rgba(198, 241, 53, 0.25) !important;
    }
    .stButton > button:hover {
        background: #B8E22E !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(198, 241, 53, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* ==================== MENU BUTTON ==================== */
    .menu-button {
        position: fixed;
        top: 16px;
        left: 16px;
        width: 48px;
        height: 48px;
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 999;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .menu-button:hover {
        background: #F5F5F7;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        transform: scale(1.05);
    }
    .menu-button:active {
        transform: scale(0.95);
    }
    .menu-icon {
        width: 24px;
        height: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .menu-line {
        width: 100%;
        height: 2px;
        background: #1D1D1F;
        border-radius: 1px;
        transition: all 0.3s ease;
    }

    /* ==================== DOWNLOAD BUTTON ==================== */
    .stDownloadButton > button {
        background: #1D1D1F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;
    }
    .stDownloadButton > button:hover {
        background: #333336 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
    }

    /* ==================== STATUS MESSAGES ==================== */
    .stSuccess > div {
        background: rgba(198, 241, 53, 0.08) !important;
        border: 1px solid rgba(198, 241, 53, 0.25) !important;
        border-radius: 14px !important;
        color: #1D1D1F !important;
    }
    .stError > div {
        background: rgba(255, 59, 48, 0.06) !important;
        border: 1px solid rgba(255, 59, 48, 0.15) !important;
        border-radius: 14px !important;
    }
    .stWarning > div {
        background: rgba(255, 204, 0, 0.06) !important;
        border: 1px solid rgba(255, 204, 0, 0.2) !important;
        border-radius: 14px !important;
    }

    /* ==================== COLOR PICKER ==================== */
    .stColorPicker > div {
        background: transparent !important;
    }
    .stColorPicker > div > div > div > div {
        border-radius: 10px !important;
        border: 1.5px solid rgba(0, 0, 0, 0.08) !important;
    }

    /* ==================== DIVIDER ==================== */
    hr {
        border-color: rgba(0, 0, 0, 0.05) !important;
        margin: 20px 0 !important;
    }

    /* ==================== SIDEBAR BADGES ==================== */
    .tech-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 600;
        margin: 3px 2px;
        background: rgba(0, 0, 0, 0.04);
        color: #6E6E73;
        border: 1px solid rgba(0, 0, 0, 0.06);
        letter-spacing: 0.2px;
    }
    .tech-pill-active {
        background: rgba(198, 241, 53, 0.15);
        color: #4A7A00;
        border: 1px solid rgba(198, 241, 53, 0.3);
    }

    /* Sidebar nav item */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 4px;
        color: #6E6E73;
        font-size: 0.88rem;
        font-weight: 500;
        transition: all 0.2s ease;
        cursor: default;
    }
    .nav-item-active {
        background: rgba(198, 241, 53, 0.12);
        color: #1D1D1F;
        font-weight: 600;
    }
    .nav-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #D1D1D6;
    }
    .nav-dot-active {
        background: #C6F135;
        box-shadow: 0 0 6px rgba(198, 241, 53, 0.5);
    }

    /* ==================== SPINNER ==================== */
    .stSpinner > div {
        color: #6E6E73 !important;
    }

    /* ==================== HIDE STREAMLIT CHROME ==================== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ==================== METRIC DISPLAY ==================== */
    .metric-row {
        display: flex;
        gap: 12px;
        margin-top: 12px;
    }
    .metric-item {
        flex: 1;
        background: #F5F5F7;
        border-radius: 14px;
        padding: 14px 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1D1D1F;
        letter-spacing: -0.5px;
    }
    .metric-label {
        font-size: 0.68rem;
        font-weight: 600;
        color: #AEAEB2;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }

    /* ==================== STATUS INDICATOR ==================== */
    .status-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        background: rgba(52, 199, 89, 0.08);
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34C759;
        animation: statusPulse 2s ease-in-out infinite;
    }
    @keyframes statusPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.85); }
    }
    .status-text {
        font-size: 0.78rem;
        font-weight: 600;
        color: #1D1D1F;
        letter-spacing: -0.1px;
    }
    </style>

    <!-- Menu Button HTML -->
    <button class="menu-button" onclick="document.querySelector('[data-testid=stSidebar]').style.display='block'" title="Show Navigation">
        <div class="menu-icon">
            <div class="menu-line"></div>
            <div class="menu-line"></div>
            <div class="menu-line"></div>
        </div>
    </button>
    """, unsafe_allow_html=True)

# 3. SIDEBAR — Navigation + Info
with st.sidebar:
    # Logo area
    st.markdown("""
        <div style="padding: 24px 8px 20px 8px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                <div style="width: 36px; height: 36px; background: #C6F135; border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            font-size: 1.1rem; font-weight: 800; color: #1D1D1F;">Q</div>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #1D1D1F; letter-spacing: -0.5px;">
                        QR Gen</div>
                    <div style="font-size: 0.65rem; font-weight: 500; color: #AEAEB2; letter-spacing: 0.5px;">
                        DEVOPS STUDIO</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    st.markdown("""
        <div style="padding: 0 8px;">
            <div class="nav-item nav-item-active">
                <div class="nav-dot nav-dot-active"></div>
                Generator
            </div>
            <div class="nav-item">
                <div class="nav-dot"></div>
                API Docs
            </div>
            <div class="nav-item">
                <div class="nav-dot"></div>
                Health Monitor
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Tech stack
    st.markdown("""
        <div style="padding: 0 8px;">
            <div style="font-size: 0.68rem; font-weight: 700; color: #AEAEB2; 
                        text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;">
                Stack</div>
            <span class="tech-pill tech-pill-active">Docker</span>
            <span class="tech-pill">FastAPI</span>
            <span class="tech-pill tech-pill-active">Streamlit</span>
            <span class="tech-pill">GitHub Actions</span>
            <span class="tech-pill">Trivy</span>
            <span class="tech-pill">CycloneDX</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Footer
    st.markdown("""
        <div style="padding: 0 8px; text-align: center;">
            <div style="font-size: 0.7rem; color: #AEAEB2; line-height: 1.8;">
                JUNIA 2026 — M2 Project<br/>
                V. Damery · H. Many · E. Peres
            </div>
        </div>
    """, unsafe_allow_html=True)


# 4. MAIN CONTENT

# Menu button to open sidebar
st.markdown("""
    <script>
    function toggleSidebar() {
        const sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
        }
    }
    </script>
""", unsafe_allow_html=True)

# Status bar
st.markdown("""
    <div class="status-bar">
        <div class="status-dot"></div>
        <span class="status-text">All systems operational — Pipeline healthy</span>
    </div>
""", unsafe_allow_html=True)

# Hero
st.markdown('<div class="hero-title">Generate QR Codes.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Enter a URL, customize the output, and let our Docker worker pipeline handle the rest.</div>', unsafe_allow_html=True)

# Bento grid layout
col_left, col_right = st.columns([3, 2], gap="medium")

with col_left:
    # URL input card
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">INPUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Target URL</div>', unsafe_allow_html=True)
    url_input = st.text_input(
        "URL", "https://youtube.com",
        label_visibility="collapsed",
        placeholder="Paste any URL here..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Customization card
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">DESIGN</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Appearance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fill_color = st.color_picker("Foreground", "#1D1D1F")
    with c2:
        back_color = st.color_picker("Background", "#FFFFFF")

    box_size = st.slider("Module size (px)", min_value=1, max_value=50, value=10)
    border = st.slider("Quiet zone (modules)", min_value=0, max_value=20, value=4)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Settings card
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">SETTINGS</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Error Correction</div>', unsafe_allow_html=True)
    error_correction = st.selectbox(
        "Level",
        options=["L", "M", "Q", "H"],
        index=1,
        label_visibility="collapsed"
    )
    st.markdown("""
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-value">L</div>
                <div class="metric-label">7% Recovery</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">M</div>
                <div class="metric-label">15% Recovery</div>
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-value">Q</div>
                <div class="metric-label">25% Recovery</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">H</div>
                <div class="metric-label">30% Recovery</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Architecture card
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">PIPELINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">How it works</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="font-size: 0.82rem; color: #6E6E73; line-height: 2;">
            <strong style="color: #1D1D1F;">1.</strong> Frontend sends request<br/>
            <strong style="color: #1D1D1F;">2.</strong> API launches Worker container<br/>
            <strong style="color: #1D1D1F;">3.</strong> Worker generates QR image<br/>
            <strong style="color: #1D1D1F;">4.</strong> API returns PNG to client
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Generate button — full width
st.markdown("")
generate_btn = st.button("GENERATE QR CODE")

# API call
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if generate_btn:
    if url_input:
        with st.spinner("Spinning up worker container..."):
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

                    st.success(f"Generated in {elapsed}s")

                    # Result card
                    st.markdown('<div class="bento-card-result">', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">OUTPUT</div>', unsafe_allow_html=True)

                    r1, r2 = st.columns([2, 3])
                    with r1:
                        st.image(image, use_container_width=True)
                    with r2:
                        st.markdown(f"""
                            <div style="padding: 8px 0;">
                                <div class="card-title">Your QR Code</div>
                                <div style="font-size: 0.82rem; color: #6E6E73; line-height: 2.2;">
                                    <strong style="color:#1D1D1F;">URL:</strong> {url_input}<br/>
                                    <strong style="color:#1D1D1F;">Colors:</strong> {fill_color} on {back_color}<br/>
                                    <strong style="color:#1D1D1F;">Module:</strong> {box_size}px · Border {border}<br/>
                                    <strong style="color:#1D1D1F;">EC Level:</strong> {error_correction}<br/>
                                    <strong style="color:#1D1D1F;">Latency:</strong> {elapsed}s
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        st.download_button(
                            label="Download PNG",
                            data=image_data,
                            file_name="qrcode.png",
                            mime="image/png",
                            use_container_width=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"API returned status {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the API. Ensure Docker containers are running.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")