import streamlit as st
from openai import OpenAI
from PIL import Image
import os
import base64
import io
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhotoMentor AI",
    page_icon=":camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #f0a500;
        text-align: center;
        letter-spacing: 1px;
    }
    .hero-sub {
        font-size: 1rem;
        color: #aaa;
        text-align: center;
        margin-top: -10px;
    }
    .upload-hint {
        color: #888;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 6px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #f0a500, #e07b00);
        color: #000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton>button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)


# ── OpenAI client ─────────────────────────────────────────────────────────────
def get_client():
    api_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("api_key", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


# ── Image → base64 ────────────────────────────────────────────────────────────
def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    fmt = image.format or "JPEG"
    if fmt not in ("JPEG", "PNG", "WEBP"):
        fmt = "JPEG"
    image.save(buffer, format=fmt)
    return base64.b64encode(buffer.getvalue()).decode("utf-8"), fmt.lower()


# ── Prompt ────────────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """
You are PhotoMentor, an expert photography coach helping beginners learn from real images.

Analyse the provided image carefully and respond in the following structured format.
Use clear, beginner-friendly language. Be specific — mention actual values where you can estimate them.

---

## 🔆 Lighting Analysis
Describe the lighting in the image:
- Type of light (natural, artificial, studio, golden hour, etc.)
- Direction (front, side, backlight, top, Rembrandt, etc.)
- Quality (hard / soft / diffused) and why
- How the light creates mood or depth in this shot

---

## 📷 Estimated Camera Settings
Based on the image, estimate the likely settings used:
- **Aperture (f-stop):** e.g., f/1.8 — explain the depth-of-field effect visible
- **Shutter Speed:** e.g., 1/500s — explain motion freeze or blur
- **ISO:** e.g., ISO 400 — comment on noise level
- **Focal Length:** e.g., 50mm — explain perspective compression
- **White Balance:** e.g., Daylight 5500K — note the colour temperature

---

## 💡 How to Recreate This Shot
Step-by-step guide for a beginner to recreate this image:
1. Equipment needed (camera type, lens, accessories)
2. Lighting setup instructions (gear or natural light positioning)
3. Camera settings to dial in
4. Composition tips (rule of thirds, leading lines, framing, etc.)
5. Post-processing hints (contrast, colour grade, etc.)

---

## 🏆 Pro Tips
3–4 advanced insights that elevate this kind of shot:
- Specific techniques visible in the image
- Common beginner mistakes to avoid for this style
- Creative variations to experiment with

---

## 🎓 Recommended Online Photography Courses
Suggest 4 relevant free or affordable online courses/resources matched to the style of this image.
For each, include:
- **Platform & Course Name**
- **Why it's relevant** to this image style
- **Link hint** (e.g., "Search on YouTube: ...", or "Available on Coursera / Udemy / Skillshare")
- **Cost**: Free / Paid (with estimated price if paid)

---

End with one encouraging sentence for the beginner.
"""


# ── Analysis ──────────────────────────────────────────────────────────────────
def analyse_image(client: OpenAI, image: Image.Image, extra_context: str = "") -> str:
    b64, fmt = image_to_base64(image)
    prompt = ANALYSIS_PROMPT
    if extra_context.strip():
        prompt += f"\n\nExtra context from the user: {extra_context.strip()}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{fmt};base64,{b64}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Get a key at platform.openai.com",
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("API key saved for this session.")

    st.markdown("---")
    st.markdown("### How to get an API key")
    st.markdown(
        """
1. Go to **platform.openai.com**
2. Sign in → **API Keys → Create new secret key**
3. Paste it above

**Cost:** ~$0.001 per analysis (very cheap)
        """
    )
    st.markdown("---")
    st.markdown("### What PhotoMentor analyses")
    st.markdown(
        """
- Lighting type & direction
- Estimated camera settings
- Step-by-step recreation guide
- Pro photographer tips
- Recommended courses
        """
    )
    st.markdown("---")
    st.caption("Powered by OpenAI GPT-4o Mini")


# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">📷 PhotoMentor AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Upload any photo — AI or captured — and learn how to master it.</div>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

col_upload, col_result = st.columns([1, 1.4], gap="large")

with col_upload:
    st.markdown("#### Upload Your Image")
    uploaded_file = st.file_uploader(
        "Drop an image here",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="upload-hint">Supports JPG, PNG, WEBP · Max 20 MB</div>',
        unsafe_allow_html=True,
    )

    extra_context = st.text_area(
        "Optional: add context (e.g. 'this is a portrait taken indoors')",
        placeholder="Any extra info about the photo…",
        height=90,
    )

    analyse_btn = st.button("Analyse Photo", disabled=uploaded_file is None)

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_container_width=True)

with col_result:
    st.markdown("#### AI Photography Analysis")

    if not uploaded_file:
        st.info("Upload a photo on the left to get started.")

    elif analyse_btn:
        client = get_client()
        if not client:
            st.error("No API key found. Please enter your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Analysing your photo… this takes 10–20 seconds"):
                try:
                    result = analyse_image(client, image, extra_context)
                    st.session_state["last_result"] = result
                    st.session_state["last_image_name"] = uploaded_file.name
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    if "last_result" in st.session_state:
        st.markdown(st.session_state["last_result"])
        st.download_button(
            label="Download Analysis as .txt",
            data=st.session_state["last_result"],
            file_name=f"photomentor_{st.session_state.get('last_image_name', 'analysis')}.txt",
            mime="text/plain",
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>PhotoMentor AI · Built with Streamlit & OpenAI GPT-4o Mini</small></center>",
    unsafe_allow_html=True,
)
