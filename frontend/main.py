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

# 2. PREMIUM DESIGN SYSTEM — VERCEL / LINEAR INSPIRED
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ==================== RESET & GLOBAL ==================== */
    .stApp {
        background: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }

    /* Hide ALL Streamlit chrome */
    #MainMenu, footer, header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    .reportview-container .main footer,
    div[data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
    }
    button[kind="header"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        padding: 3rem 1rem 2rem 1rem !important;
        max-width: 720px !important;
    }

    /* ==================== FLOATING CARD ==================== */
    .main-card {
        display : none;
    }
    .main-card:hover {
        box-shadow:
            0 2px 4px rgba(0, 0, 0, 0.04),
            0 8px 24px rgba(0, 0, 0, 0.06),
            0 16px 56px rgba(0, 0, 0, 0.05);
    }

    /* ==================== RESULT CARD — ANIMATED ==================== */
    .result-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 20px;
        padding: 40px 36px;
        margin-top: 20px;
        box-shadow:
            0 1px 2px rgba(0, 0, 0, 0.04),
            0 8px 32px rgba(0, 0, 0, 0.06);
        animation: cardReveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes cardReveal {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.97);
            filter: blur(4px);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }

    /* QR image animation */
    .qr-reveal {
        animation: qrFadeScale 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards;
        opacity: 0;
    }
    @keyframes qrFadeScale {
        0% {
            opacity: 0;
            transform: scale(0.88) rotate(-2deg);
            filter: blur(6px);
        }
        60% {
            transform: scale(1.02) rotate(0deg);
            filter: blur(0);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
            filter: blur(0);
        }
    }

    /* ==================== BRAND HEADER ==================== */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 8px;
    }
    .brand-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #111827 0%, #374151 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        box-shadow: 0 2px 8px rgba(17, 24, 39, 0.25);
    }
    .brand-text {
        font-size: 1.3rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -1px;
    }
    .brand-badge {
        font-size: 0.6rem;
        font-weight: 700;
        color: #6B7280;
        background: rgba(107, 114, 128, 0.08);
        padding: 3px 10px;
        border-radius: 100px;
        border: 1px solid rgba(107, 114, 128, 0.12);
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .page-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: #111827;
        line-height: 1.1;
        margin-bottom: 6px;
        margin-top: 20px;
    }
    .page-subtitle {
        text-align: center;
        font-size: 1.02rem;
        font-weight: 400;
        color: #9CA3AF;
        letter-spacing: -0.2px;
        line-height: 1.6;
        margin-bottom: 32px;
    }

    /* ==================== SECTION LABELS ==================== */
    .label-sm {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #9CA3AF;
        margin-bottom: 14px;
    }
    .label-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }

    /* ==================== FORM ELEMENTS ==================== */
    .stTextInput > div > div > input {
        background: #F9FAFB !important;
        color: #111827 !important;
        border: 1.5px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 15px 20px !important;
        font-size: 0.98rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.25s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 4px rgba(17, 24, 39, 0.08) !important;
        background: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #C4C9D4 !important;
    }

    /* Labels */
    .stTextInput label, .stSlider label, .stSelectbox label, .stColorPicker label,
    div[data-testid="stWidgetLabel"] label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: -0.1px !important;
    }

    /* Slider */
    .stSlider > div > div > div > div {
        background: #111827 !important;
    }
    .stSlider > div > div > div {
        background: #E5E7EB !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #F9FAFB !important;
        border: 1.5px solid #E5E7EB !important;
        border-radius: 14px !important;
        color: #111827 !important;
    }

    /* Color picker */
    .stColorPicker > div {
        background: transparent !important;
    }
    .stColorPicker > div > div > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #E5E7EB !important;
    }

    /* ==================== CTA BUTTON — DARK PREMIUM ==================== */
    .stButton > button {
        width: 100%;
        background: #111827 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        height: 54px !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 2px 8px rgba(17, 24, 39, 0.2), 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        background: #1F2937 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(17, 24, 39, 0.35), 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
        box-shadow: 0 2px 8px rgba(17, 24, 39, 0.2) !important;
    }

    /* ==================== DOWNLOAD BUTTON ==================== */
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1.5px solid #E5E7EB !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    }
    .stDownloadButton > button:hover {
        background: #F9FAFB !important;
        border-color: #111827 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    /* ==================== STATUS MESSAGES ==================== */
    .stSuccess > div {
        background: rgba(16, 185, 129, 0.06) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 14px !important;
        color: #065F46 !important;
    }
    .stError > div {
        background: rgba(239, 68, 68, 0.06) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 14px !important;
    }
    .stWarning > div {
        background: rgba(245, 158, 11, 0.06) !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-radius: 14px !important;
    }

    /* ==================== DIVIDER ==================== */
    .divider {
        height: 1px;
        background: #F3F4F6;
        margin: 28px 0;
        border: none;
    }
    hr {
        border-color: #F3F4F6 !important;
        margin: 24px 0 !important;
    }

    /* ==================== METRIC CHIPS ==================== */
    .metric-row {
        display: flex;
        gap: 10px;
        margin-top: 14px;
    }
    .metric-chip {
        flex: 1;
        background: #F9FAFB;
        border: 1px solid #F3F4F6;
        border-radius: 14px;
        padding: 14px 12px;
        text-align: center;
        transition: all 0.25s ease;
    }
    .metric-chip:hover {
        border-color: #E5E7EB;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .metric-chip-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.5px;
    }
    .metric-chip-label {
        font-size: 0.65rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 3px;
    }

    /* ==================== DETAIL ROW ==================== */
    .detail-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #F9FAFB;
        font-size: 0.86rem;
    }
    .detail-row:last-child {
        border-bottom: none;
    }
    .detail-key {
        font-weight: 600;
        color: #6B7280;
    }
    .detail-value {
        font-weight: 600;
        color: #111827;
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 0.82rem;
    }

    /* ==================== STATUS DOT ==================== */
    .status-inline {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-bottom: 28px;
    }
    .dot-live {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10B981;
        animation: dotPulse 2.5s ease-in-out infinite;
    }
    @keyframes dotPulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        50% { opacity: 0.7; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0); }
    }
    .status-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6B7280;
        letter-spacing: 0.2px;
    }

    /* ==================== TECH FOOTER ==================== */
    .tech-footer {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 28px;
    }
    .tech-tag {
        font-size: 0.68rem;
        font-weight: 600;
        color: #9CA3AF;
        background: rgba(156, 163, 175, 0.08);
        border: 1px solid rgba(156, 163, 175, 0.12);
        padding: 4px 12px;
        border-radius: 100px;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }
    .tech-tag:hover {
        color: #6B7280;
        border-color: rgba(156, 163, 175, 0.25);
    }

    /* ==================== SPINNER ==================== */
    .stSpinner > div {
        color: #6B7280 !important;
    }

    /* ==================== QR FRAME ==================== */
    .qr-frame {
        background: #FAFAFA;
        border: 1px solid #F3F4F6;
        border-radius: 16px;
        padding: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. BRAND HEADER
# ─────────────────────────────────────────────
st.markdown("""
    <div class="brand-bar">
        <div class="brand-icon">Q</div>
        <span class="brand-text">QR Gen</span>
        <span class="brand-badge">DevOps</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="status-inline">
        <div class="dot-live"></div>
        <span class="status-label">All systems operational</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Generate a QR Code.</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Paste a URL, customize the output, and download a production-ready QR image.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4. INPUT CARD
# ─────────────────────────────────────────────
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="label-sm">INPUT</div>', unsafe_allow_html=True)
st.markdown('<div class="label-title">Target URL</div>', unsafe_allow_html=True)

url_input = st.text_input(
    "URL", "https://youtube.com",
    label_visibility="collapsed",
    placeholder="https://example.com"
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="label-sm">DESIGN</div>', unsafe_allow_html=True)
st.markdown('<div class="label-title">Appearance</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    fill_color = st.color_picker("Foreground", "#111827")
with c2:
    back_color = st.color_picker("Background", "#FFFFFF")

box_size = st.slider("Module size (px)", min_value=1, max_value=50, value=10)
border = st.slider("Quiet zone (modules)", min_value=0, max_value=20, value=4)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="label-sm">ERROR CORRECTION</div>', unsafe_allow_html=True)

error_correction = st.selectbox(
    "Level",
    options=["L", "M", "Q", "H"],
    index=1,
    label_visibility="collapsed"
)

st.markdown("""
    <div class="metric-row">
        <div class="metric-chip">
            <div class="metric-chip-value">L</div>
            <div class="metric-chip-label">7% Recovery</div>
        </div>
        <div class="metric-chip">
            <div class="metric-chip-value">M</div>
            <div class="metric-chip-label">15% Recovery</div>
        </div>
        <div class="metric-chip">
            <div class="metric-chip-value">Q</div>
            <div class="metric-chip-label">25% Recovery</div>
        </div>
        <div class="metric-chip">
            <div class="metric-chip-value">H</div>
            <div class="metric-chip-label">30% Recovery</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 5. GENERATE BUTTON
# ─────────────────────────────────────────────
st.markdown("")
generate_btn = st.button("GENERATE QR CODE")


# ─────────────────────────────────────────────
# 6. API CALL & RESULT
# ─────────────────────────────────────────────
API_URL = os.environ.get("API_URL", "http://localhost:8000/generate")

if generate_btn:
    if url_input:
        with st.spinner("Generating via worker container…"):
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

                    st.success(f"✓ Generated in {elapsed}s")

                    # Result card with animations
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<div class="label-sm">OUTPUT</div>', unsafe_allow_html=True)
                    st.markdown('<div class="label-title">Your QR Code</div>', unsafe_allow_html=True)

                    col_qr, col_info = st.columns([1, 1])

                    with col_qr:
                        st.markdown('<div class="qr-frame qr-reveal">', unsafe_allow_html=True)
                        st.image(image, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col_info:
                        st.markdown(f"""
                            <div style="padding: 4px 0;">
                                <div class="detail-row">
                                    <span class="detail-key">URL</span>
                                    <span class="detail-value">{url_input[:35]}{'…' if len(url_input) > 35 else ''}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-key">Colors</span>
                                    <span class="detail-value">{fill_color} / {back_color}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-key">Module</span>
                                    <span class="detail-value">{box_size}px</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-key">Border</span>
                                    <span class="detail-value">{border} modules</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-key">EC Level</span>
                                    <span class="detail-value">{error_correction}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-key">Latency</span>
                                    <span class="detail-value">{elapsed}s</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown("")
                        st.download_button(
                            label="↓  Download PNG",
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


# ─────────────────────────────────────────────
# 7. FOOTER
# ─────────────────────────────────────────────
st.markdown("""
    <div class="tech-footer">
        <span class="tech-tag">Docker</span>
        <span class="tech-tag">FastAPI</span>
        <span class="tech-tag">Streamlit</span>
        <span class="tech-tag">GitHub Actions</span>
        <span class="tech-tag">Trivy</span>
        <span class="tech-tag">CycloneDX</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: 24px; padding-bottom: 16px;">
        <div style="font-size: 0.7rem; color: #C4C9D4; font-weight: 500; letter-spacing: 0.2px;">
            JUNIA 2026 — M2 Project · V. Damery · H. Many · E. Peres
        </div>
    </div>
""", unsafe_allow_html=True)