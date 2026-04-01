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
    page_title="PhotoMentor AI",
    page_icon=":camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e8e8e8; }

    /* Hide default streamlit branding */
    #MainMenu, footer { visibility: hidden; }

    /* Hero */
    .hero { text-align: center; padding: 1.5rem 0 0.5rem 0; }
    .hero h1 { font-size: 2rem; font-weight: 800; color: #f0a500; margin: 0; }
    .hero p  { color: #888; font-size: 0.95rem; margin-top: 4px; }

    /* Chat bubbles */
    .bubble-user {
        background: #1e293b;
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 85%;
        margin-left: auto;
        color: #e2e8f0;
        font-size: 0.9rem;
    }
    .bubble-ai {
        background: #1a1f2e;
        border-left: 3px solid #f0a500;
        border-radius: 4px 16px 16px 16px;
        padding: 14px 18px;
        margin: 8px 0;
        max-width: 95%;
        color: #e2e8f0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .bubble-ai h2 {
        font-size: 0.95rem;
        color: #f0a500;
        margin: 14px 0 4px 0;
        border-bottom: 1px solid #2a2f3e;
        padding-bottom: 4px;
    }
    .bubble-ai ul { padding-left: 18px; margin: 4px 0; }
    .bubble-ai li { margin-bottom: 3px; }
    .bubble-ai strong { color: #fbbf24; }

    /* Tag badges */
    .tag {
        display: inline-block;
        background: #252840;
        border: 1px solid #f0a500;
        color: #f0a500;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin: 2px 3px;
    }

    /* Upload area */
    .upload-box {
        background: #161b27;
        border: 1.5px dashed #2d3748;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }

    /* Analyse button */
    .stButton > button {
        background: linear-gradient(90deg, #f0a500, #e07b00);
        color: #000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
        font-size: 0.95rem;
    }
    .stButton > button:hover { opacity: 0.88; }
    .stButton > button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_client():
    # Priority: sidebar input → .env → Streamlit Cloud secrets
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

# ── Prompt ────────────────────────────────────────────────────────────────────
PROMPT = """
You are PhotoMentor, a friendly expert photography coach. Analyse the image and reply in this exact format — keep each section SHORT and punchy (2-4 bullet points max per section). Use simple language for beginners.

## ✨ Shot Summary
One sentence describing what kind of shot this is and what makes it work.

## 🔆 Lighting
- Light type & direction (e.g. "Soft side light from a window")
- Quality: hard / soft / diffused
- Mood it creates

## 📷 Camera Settings (estimated)
- **Aperture:** f/X — [effect]
- **Shutter:** 1/Xs
- **ISO:** X
- **Focal Length:** Xmm

## 💡 How to Recreate
3 clear steps a beginner can follow right now.

## 🏆 Pro Tip
One standout technique used in this shot. One common mistake to avoid.

## 🎓 Learn More
2 course recommendations relevant to this style:
- **[Platform] Course Name** — why it fits · Free / ~$X

Keep the whole response under 350 words. End with one short motivating line.
"""

def analyse_image(client, image: Image.Image, extra_context: str = "") -> str:
    b64, fmt = image_to_base64(image)
    prompt = PROMPT
    if extra_context.strip():
        prompt += f"\n\nUser note: {extra_context.strip()}"
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

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")
    api_key_input = st.text_input(
        "OpenAI API Key", type="password", placeholder="sk-..."
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("Key saved.")

    st.markdown("---")
    st.markdown("""
**Get a key:**
1. Go to **platform.openai.com**
2. API Keys → Create new key
3. Paste above

**Cost:** ~$0.001 per photo
""")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("PhotoMentor AI · GPT-4o Mini")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>📷 PhotoMentor AI</h1>
  <p>Upload a photo and get instant photography coaching</p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            if msg.get("image"):
                st.image(msg["image"], width=280)
            st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

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
        "Add context (optional)",
        placeholder="e.g. 'taken at sunset with a phone'…",
        height=80,
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

        # Add user message to history
        user_text = f"Analyse this photo{': ' + extra_context.strip() if extra_context.strip() else '.'}"
        st.session_state.messages.append({
            "role": "user",
            "content": user_text,
            "image": image.copy()
        })

        with st.spinner("Analysing your photo…"):
            try:
                result = analyse_image(client, image, extra_context)
                # Convert markdown to HTML-safe for bubble rendering
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, analysis failed: {e}"
                })

        st.rerun()

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div style="text-align:center; padding: 2rem 0; color: #555;">
  <div style="font-size: 3rem;">📷</div>
  <div style="font-size: 1rem; margin-top: 8px;">Upload a photo below to get started</div>
  <div style="margin-top: 12px;">
    <span class="tag">Lighting Analysis</span>
    <span class="tag">Camera Settings</span>
    <span class="tag">Pro Tips</span>
    <span class="tag">Course Picks</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<center><small style='color:#444'>PhotoMentor AI · Built with Streamlit & Yahya</small></center>",
    unsafe_allow_html=True,
)
