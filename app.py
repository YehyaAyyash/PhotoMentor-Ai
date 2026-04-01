import streamlit as st
from openai import OpenAI
from PIL import Image
import os
import base64
import io
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PixelPulse Innovation AI",
    page_icon="assets/logo.png" if os.path.exists("assets/logo.png") else ":camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand colours ─────────────────────────────────────────────────────────────
PRIMARY   = "#8FD14F"   # brand green
PRIMARY_L = "#a3e063"   # lighter green (hover / glow)
BG        = "#0d0d0d"   # page background
BG2       = "#141414"   # card / bubble background
BG3       = "#1a1a1a"   # input / sidebar background
BORDER    = "#1f1f1f"   # subtle border
TEXT      = "#e4e4e4"
MUTED     = "#666666"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, .stApp {{
        background-color: {BG};
        color: {TEXT};
        font-family: 'Inter', sans-serif;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: {BG}; }}
    ::-webkit-scrollbar-thumb {{ background: {PRIMARY}; border-radius: 4px; }}

    /* Hide Streamlit chrome */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1rem !important; }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {BG3} !important;
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

    /* ── Logo / Hero ── */
    .brand-header {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        padding: 1.2rem 0 0.4rem 0;
    }}
    .brand-header img {{
        height: 52px;
        width: 52px;
        object-fit: contain;
        border-radius: 10px;
        border: 1.5px solid {PRIMARY};
        padding: 4px;
        background: #111;
    }}
    .brand-title {{
        font-size: 1.7rem;
        font-weight: 800;
        color: {PRIMARY};
        letter-spacing: -0.5px;
        line-height: 1.1;
    }}
    .brand-sub {{
        font-size: 0.75rem;
        color: {MUTED};
        margin-top: 2px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    .brand-tagline {{
        text-align: center;
        color: {MUTED};
        font-size: 0.88rem;
        padding-bottom: 0.8rem;
    }}

    /* ── Divider ── */
    hr {{ border-color: {BORDER} !important; }}

    /* ── Chat bubbles ── */
    .bubble-user {{
        background: #1b2b1b;
        border: 1px solid {PRIMARY}44;
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px;
        margin: 8px 0 8px auto;
        max-width: 82%;
        color: {TEXT};
        font-size: 0.88rem;
    }}
    .bubble-ai {{
        background: {BG2};
        border-left: 3px solid {PRIMARY};
        border-radius: 4px 16px 16px 16px;
        padding: 14px 18px;
        margin: 8px 0;
        max-width: 96%;
        color: {TEXT};
        font-size: 0.88rem;
        line-height: 1.65;
        box-shadow: 0 2px 12px #00000033;
    }}
    .bubble-ai h2 {{
        font-size: 0.88rem;
        font-weight: 700;
        color: {PRIMARY_L};
        margin: 12px 0 4px 0;
        border-bottom: 1px solid {BORDER};
        padding-bottom: 3px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    .bubble-ai ul {{ padding-left: 16px; margin: 4px 0 8px 0; }}
    .bubble-ai li {{ margin-bottom: 4px; }}
    .bubble-ai strong {{ color: #5dba52; }}

    /* ── Avatar chips ── */
    .avatar-ppi {{
        display: inline-block;
        background: {PRIMARY};
        color: #fff;
        font-weight: 800;
        font-size: 0.7rem;
        border-radius: 50%;
        width: 26px; height: 26px;
        line-height: 26px;
        text-align: center;
        margin-right: 6px;
        vertical-align: middle;
        flex-shrink: 0;
    }}
    .msg-row {{
        display: flex;
        align-items: flex-start;
        gap: 8px;
        margin: 6px 0;
    }}

    /* ── Tag badges ── */
    .tag {{
        display: inline-block;
        background: #1b2b1b;
        border: 1px solid {PRIMARY}66;
        color: {PRIMARY_L};
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.74rem;
        margin: 3px 4px;
        font-weight: 600;
    }}

    /* ── Analyse button ── */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_L});
        color: #fff !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 11px;
        font-size: 0.92rem;
        letter-spacing: 0.3px;
        transition: all 0.2s;
        box-shadow: 0 0 12px {PRIMARY}55;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 20px {PRIMARY}99;
        transform: translateY(-1px);
    }}
    .stButton > button:disabled {{
        opacity: 0.3;
        cursor: not-allowed;
        box-shadow: none;
    }}

    /* ── File uploader & textarea ── */
    [data-testid="stFileUploader"] {{
        background: {BG3};
        border: 1.5px dashed {PRIMARY}55;
        border-radius: 10px;
        padding: 10px;
    }}
    textarea {{
        background: {BG3} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT} !important;
        border-radius: 8px !important;
    }}

    /* ── Empty state ── */
    .empty-state {{
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        color: #333;
    }}
    .empty-icon {{
        font-size: 3.5rem;
        filter: grayscale(0.3);
    }}
    .empty-text {{
        font-size: 0.95rem;
        color: #444;
        margin-top: 10px;
    }}

    /* ── Spinner ── */
    .stSpinner > div {{ border-top-color: {PRIMARY} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_client():
    api_key = (
        st.session_state.get("api_key")
        or os.getenv("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY", "")
    )
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def image_to_base64(image: Image.Image):
    buffer = io.BytesIO()
    fmt = image.format or "JPEG"
    if fmt not in ("JPEG", "PNG", "WEBP"):
        fmt = "JPEG"
    image.save(buffer, format=fmt)
    return base64.b64encode(buffer.getvalue()).decode(), fmt.lower()

def logo_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ── Prompt ────────────────────────────────────────────────────────────────────
PROMPT = """
You are PixelPulse AI, a friendly expert photography coach. Analyse the image and reply in this exact format.
Keep each section SHORT and punchy (2-4 bullet points max). Use simple language for beginners.

## ✨ Shot Summary
One sentence: what kind of shot this is and what makes it stand out.

## 🔆 Lighting
- Light type & direction (e.g. "Soft window side-light")
- Quality: hard / soft / diffused
- Mood it creates

## 📷 Camera Settings (estimated)
- **Aperture:** f/X — [depth of field effect]
- **Shutter:** 1/Xs
- **ISO:** X
- **Focal Length:** Xmm

## 💡 How to Recreate
3 clear steps a beginner can follow right now.

## 🏆 Pro Tip
One standout technique used. One common beginner mistake to avoid.

## 🎓 Learn More
2 course picks matched to this style:
- **[Platform] Course Name** — why it fits · Free / ~$X

Under 350 words total. End with one short motivating line.
"""

def analyse_image(client, image: Image.Image, extra_context: str = "") -> str:
    b64, fmt = image_to_base64(image)
    prompt = PROMPT + (f"\n\nUser note: {extra_context.strip()}" if extra_context.strip() else "")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/{fmt};base64,{b64}",
                    "detail": "high"
                }},
            ],
        }],
        max_tokens=700,
    )
    return resp.choices[0].message.content


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + brand in sidebar
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        b64_logo = logo_to_base64(logo_path)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px 0;">
          <img src="data:image/png;base64,{b64_logo}"
               style="height:38px;width:38px;border-radius:8px;
                      border:1.5px solid #8FD14F;padding:3px;background:#111;">
          <div>
            <div style="font-weight:800;color:#8FD14F;font-size:0.95rem;line-height:1.1;">PixelPulse</div>
            <div style="font-size:0.7rem;color:#555;text-transform:uppercase;letter-spacing:0.5px;">Innovation AI</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-weight:800;color:#8FD14F;font-size:1rem;padding:8px 0 16px 0;'>PixelPulse Innovation AI</div>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Setup")
    api_key_input = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("Key saved ✓")

    st.markdown("---")
    st.markdown("""
**Get a key:**
1. Go to **platform.openai.com**
2. API Keys → Create new key
3. Paste above

**Cost:** ~$0.001 per analysis
""")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("PixelPulse Innovation AI · GPT-4o Mini")

# ── Header ────────────────────────────────────────────────────────────────────
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    b64_logo = logo_to_base64(logo_path)
    st.markdown(f"""
    <div class="brand-header">
      <img src="data:image/png;base64,{b64_logo}" alt="logo">
      <div>
        <div class="brand-title">PixelPulse Innovation AI</div>
        <div class="brand-sub">Photography Coaching · Powered by GPT-4o Mini</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="brand-header">
      <div style="background:#8FD14F;color:#fff;font-weight:900;font-size:1.1rem;
                  width:52px;height:52px;border-radius:10px;display:flex;
                  align-items:center;justify-content:center;">PPI</div>
      <div>
        <div class="brand-title">PixelPulse Innovation AI</div>
        <div class="brand-sub">Photography Coaching · Powered by GPT-4o Mini</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="brand-tagline">Upload any photo and get instant AI photography coaching</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        if msg.get("image"):
            col_sp, col_img = st.columns([0.05, 0.95])
            with col_img:
                st.image(msg["image"], width=260)
        st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row">
          <span class="avatar-ppi">AI</span>
          <div class="bubble-ai">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">📷</div>
      <div class="empty-text">Upload a photo below to get instant coaching</div>
      <div style="margin-top:14px;">
        <span class="tag">Lighting Analysis</span>
        <span class="tag">Camera Settings</span>
        <span class="tag">Recreation Guide</span>
        <span class="tag">Pro Tips</span>
        <span class="tag">Course Picks</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Input area ────────────────────────────────────────────────────────────────
st.markdown("---")
col_file, col_ctx = st.columns([1, 1.5])

with col_file:
    uploaded_file = st.file_uploader(
        "Upload photo", type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.image(uploaded_file, width=220)

with col_ctx:
    extra_context = st.text_area(
        "Add context",
        placeholder="Optional: e.g. 'portrait taken indoors at night'…",
        height=82,
        label_visibility="collapsed"
    )
    analyse_btn = st.button("📸 Analyse Photo", disabled=uploaded_file is None)

# ── On analyse ────────────────────────────────────────────────────────────────
if analyse_btn and uploaded_file:
    client = get_client()
    if not client:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        image = Image.open(uploaded_file)
        user_text = f"Analyse this photo{': ' + extra_context.strip() if extra_context.strip() else '.'}"
        st.session_state.messages.append({
            "role": "user",
            "content": user_text,
            "image": image.copy()
        })
        with st.spinner("Analysing your photo…"):
            try:
                result = analyse_image(client, image, extra_context)
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Analysis failed: {e}"
                })
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<center><small style='color:#2a2a2a;'>PixelPulse Innovation AI · Built by Yahya Ayyash</small></center>",
    unsafe_allow_html=True,
)
