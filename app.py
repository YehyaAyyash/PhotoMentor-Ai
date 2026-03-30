import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhotoMentor AI",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0e1117; }

    /* Card-style containers */
    .tip-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border-left: 4px solid #f0a500;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0;
        color: #e8e8e8;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f0a500;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }
    .course-card {
        background: linear-gradient(135deg, #1a2a1a, #1e301e);
        border-left: 4px solid #4caf50;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #d4f0d4;
    }
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


# ── Gemini setup ──────────────────────────────────────────────────────────────
def get_model():
    api_key = os.getenv("GEMINI_API_KEY") or st.session_state.get("api_key", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


# ── Prompt builder ────────────────────────────────────────────────────────────
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


# ── Analysis function ─────────────────────────────────────────────────────────
def analyse_image(model, image: Image.Image, extra_context: str = "") -> str:
    prompt = ANALYSIS_PROMPT
    if extra_context.strip():
        prompt += f"\n\nExtra context from the user: {extra_context.strip()}"
    response = model.generate_content([prompt, image])
    return response.text


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your free API key here",
        help="Get a free key at aistudio.google.com",
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("API key saved for this session.")

    st.markdown("---")
    st.markdown("### How to get a free API key")
    st.markdown(
        """
1. Go to **aistudio.google.com**
2. Sign in with your Google account
3. Click **Get API Key → Create API Key**
4. Paste it above
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
    st.caption("Powered by Google Gemini 1.5 Flash (free tier)")


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
        '<div class="upload-hint">Supports JPG, PNG, WEBP · Max 200 MB</div>',
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
        model = get_model()
        if not model:
            st.error(
                "No API key found. Please enter your Gemini API key in the sidebar."
            )
        else:
            with st.spinner("Analysing your photo… this takes 10–20 seconds"):
                try:
                    result = analyse_image(model, image, extra_context)
                    st.session_state["last_result"] = result
                    st.session_state["last_image_name"] = uploaded_file.name
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    # Render last result
    if "last_result" in st.session_state:
        result_text = st.session_state["last_result"]

        # Render as markdown (the model returns structured markdown)
        st.markdown(result_text)

        # Download button
        st.download_button(
            label="Download Analysis as .txt",
            data=result_text,
            file_name=f"photomentor_{st.session_state.get('last_image_name', 'analysis')}.txt",
            mime="text/plain",
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>PhotoMentor AI · Built with Streamlit & Google Gemini · Free to use</small></center>",
    unsafe_allow_html=True,
)
