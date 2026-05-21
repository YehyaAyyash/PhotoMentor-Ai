import streamlit as st
from openai import OpenAI
from PIL import Image
import os, base64, io
from dotenv import load_dotenv
import db
from quiz_data import CHALLENGES, DIFFICULTY_COLOR

load_dotenv()
db.init_db()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PixelPulse Innovation AI",
    page_icon="assets/logo.png" if os.path.exists("assets/logo.png") else ":camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

GREEN  = "#8FD14F"
GLOW   = "#a3e063"
BG     = "#0d0d0d"
BG2    = "#141414"
BG3    = "#1c1c1c"
BORDER = "#252525"
TEXT   = "#e4e4e4"
MUTED  = "#555"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, .stApp {{
    background: {BG};
    color: {TEXT};
    font-family: 'Inter', sans-serif;
}}
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {GREEN}55; border-radius: 4px; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0.5rem !important; padding-bottom: 6rem !important; }}

/* ── Sidebar ─────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {BG2} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] > div {{ padding-top: 0 !important; }}

.sb-brand {{
    text-align: center;
    padding: 1.4rem 1rem 1rem 1rem;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 0.5rem;
}}
.sb-brand img {{
    width: 56px; height: 56px;
    border-radius: 14px;
    border: 2px solid {GREEN};
    padding: 4px; background: #111;
    display: block; margin: 0 auto 10px auto;
    box-shadow: 0 0 18px {GREEN}33;
}}
.sb-name {{
    font-size: 0.92rem; font-weight: 800;
    color: {GREEN}; line-height: 1.2;
}}
.sb-tagline {{
    font-size: 0.65rem; color: {MUTED};
    text-transform: uppercase; letter-spacing: 0.6px;
    margin-top: 3px;
}}

[data-testid="stSidebar"] div[data-testid="stRadio"] {{
    padding: 0 0.4rem;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
    display: flex !important;
    flex-direction: column !important;
    gap: 3px;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    border-radius: 9px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: {MUTED} !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    margin: 0 !important;
    width: 100% !important;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background: #1e1e1e !important;
    color: {TEXT} !important;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] [data-baseweb="radio"] {{
    display: none !important;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background: #1b2b1b !important;
    color: {GREEN} !important;
}}
[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {{
    color: {GREEN} !important;
    font-weight: 700 !important;
}}

.sess-item {{
    background: {BG3};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 7px 10px;
    margin: 3px 0;
    font-size: 0.8rem;
    color: {TEXT};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.sess-active {{ border-color: {GREEN}66 !important; background: #1b2b1b !important; }}

[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    color: {MUTED} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    padding: 5px 10px !important;
    width: 100% !important;
    text-align: left !important;
    box-shadow: none !important;
    font-weight: 500 !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    border-color: {GREEN}55 !important;
    color: {TEXT} !important;
    transform: none !important;
}}

/* ── Greeting header (chat empty state) ──────── */
.greeting-header {{
    padding: 2rem 0.5rem 2rem 0.5rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(180deg, #0e190e 0%, {BG} 100%);
    border-bottom: 1px solid {BORDER};
}}
.greeting-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.6rem;
}}
.premium-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #1b2b1b;
    border: 1px solid {GREEN}44;
    color: {GREEN};
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.2px;
}}
.user-avatar {{
    width: 42px; height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, {GREEN}, {GLOW});
    color: #000;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 0.92rem;
    border: 2px solid {BORDER};
    box-shadow: 0 0 14px {GREEN}33;
}}
.greeting-name {{
    font-size: 2.5rem;
    font-weight: 900;
    color: {TEXT};
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 8px;
}}
.greeting-sub {{
    font-size: 0.86rem;
    color: {MUTED};
    line-height: 1.5;
    max-width: 460px;
}}

/* ── Suggestion cards ────────────────────────── */
/* suggest-btn is a sibling marker div; use :has() adjacent selector to reach the button */
.stElementContainer:has(.suggest-btn) + .stElementContainer .stButton > button,
.stElementContainer:has(.suggest-btn) + .stElementContainer [data-testid="stBaseButton-secondary"] {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 18px !important;
    padding: 20px 18px !important;
    text-align: left !important;
    width: 100% !important;
    min-height: 120px !important;
    color: #777 !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    white-space: normal !important;
    transition: border-color 0.2s, background 0.2s, color 0.2s !important;
    box-shadow: none !important;
    vertical-align: top !important;
}}
.stElementContainer:has(.suggest-btn) + .stElementContainer .stButton > button:hover,
.stElementContainer:has(.suggest-btn) + .stElementContainer [data-testid="stBaseButton-secondary"]:hover {{
    border-color: {GREEN}55 !important;
    background: #192914 !important;
    transform: none !important;
    box-shadow: 0 8px 24px #00000066 !important;
    color: {TEXT} !important;
}}
.stElementContainer:has(.suggest-btn) + .stElementContainer .stButton > button p {{
    color: inherit !important;
    font-size: 0.83rem !important;
    line-height: 1.6 !important;
}}

/* ── Chat messages ───────────────────────────── */
.bubble-user {{
    background: #1b2b1b;
    border: 1px solid {GREEN}22;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 6px 0 6px auto;
    max-width: 78%;
    color: {TEXT};
    font-size: 0.88rem;
    line-height: 1.5;
}}
.bubble-ai {{
    background: {BG2};
    border-left: 3px solid {GREEN};
    border-radius: 4px 18px 18px 18px;
    padding: 13px 17px;
    margin: 6px 0;
    max-width: 92%;
    color: {TEXT};
    font-size: 0.88rem;
    line-height: 1.65;
    box-shadow: 0 2px 16px #00000033;
}}
.bubble-ai h2 {{
    font-size: 0.8rem; font-weight: 700;
    color: {GREEN}; margin: 12px 0 4px 0;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 3px;
    text-transform: uppercase; letter-spacing: 0.5px;
}}
.bubble-ai ul {{ padding-left: 16px; margin: 4px 0 8px 0; }}
.bubble-ai li {{ margin-bottom: 4px; }}
.bubble-ai strong {{ color: {GLOW}; }}
.ai-row {{ display: flex; align-items: flex-start; gap: 8px; margin: 6px 0; }}
.ai-avatar {{
    display: inline-flex; align-items: center; justify-content: center;
    background: {GREEN}; color: #000; font-weight: 800; font-size: 0.6rem;
    border-radius: 50%; min-width: 24px; height: 24px; margin-top: 2px;
}}

/* ── Input bar — pill shape ──────────────────── */
.input-wrap {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, {BG} 80%, transparent);
    padding: 12px 24px 20px 24px;
    z-index: 100;
}}
.input-inner {{
    max-width: 760px;
    margin: 0 auto;
    background: {BG3};
    border: 1px solid #2a2a2a;
    border-radius: 50px;
    display: flex;
    align-items: flex-end;
    gap: 0;
    padding: 6px 6px 6px 14px;
    box-shadow: 0 4px 32px #00000077;
    transition: border-color 0.2s;
}}
.input-inner:focus-within {{
    border-color: {GREEN}55;
    box-shadow: 0 4px 32px {GREEN}11;
}}

/* Upload icon */
.upload-icon-wrap [data-testid="stFileUploader"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}}
.upload-icon-wrap [data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    min-height: unset !important;
    width: 38px !important;
    height: 38px !important;
    overflow: hidden !important;
}}
.upload-icon-wrap [data-testid="stFileUploaderDropzoneInstructions"] {{
    display: none !important;
}}
.upload-icon-wrap [data-testid="stFileUploaderDropzone"] svg {{
    display: none !important;
}}
.upload-icon-wrap [data-testid="stFileUploader"] button {{
    background: transparent !important;
    border: none !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    min-height: unset !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}}
.upload-icon-wrap [data-testid="stFileUploader"] button:hover {{
    background: #1b2b1b !important;
}}
.upload-icon-wrap [data-testid="stFileUploader"] button span {{
    display: none !important;
}}
.upload-icon-wrap [data-testid="stFileUploader"] button::after {{
    content: "＋";
    font-size: 1.1rem;
    font-weight: 300;
    color: {MUTED};
    line-height: 1;
}}
.upload-icon-wrap [data-testid="stFileUploader"] button:hover::after {{
    color: {GREEN};
}}
.upload-icon-wrap small {{
    display: none !important;
}}

/* Text area */
.text-wrap textarea {{
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    color: {TEXT} !important;
    font-size: 0.93rem !important;
    resize: none !important;
    padding: 6px 4px !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.5 !important;
}}
.text-wrap textarea::placeholder {{ color: {MUTED} !important; }}
.text-wrap [data-testid="stTextArea"] {{ margin: 0 !important; }}
.text-wrap [data-testid="stTextArea"] label {{ display: none !important; }}
.text-wrap [data-baseweb="textarea"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Send button — circular green */
.send-wrap .stButton > button {{
    background: {GREEN} !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 50% !important;
    width: 42px !important; height: 42px !important;
    padding: 0 !important;
    font-size: 1.15rem !important;
    min-width: unset !important;
    box-shadow: 0 0 16px {GREEN}55 !important;
    transition: all 0.15s !important;
}}
.send-wrap .stButton > button:hover {{
    background: {GLOW} !important;
    box-shadow: 0 0 26px {GREEN}99 !important;
    transform: scale(1.06) !important;
}}
.send-wrap .stButton > button:disabled {{
    opacity: 0.25 !important;
    box-shadow: none !important;
}}

/* Main action buttons */
.main-btn .stButton > button {{
    background: linear-gradient(135deg, {GREEN}, {GLOW}) !important;
    color: #000 !important; font-weight: 700 !important;
    border: none !important; border-radius: 9px !important;
    padding: 10px 20px !important; font-size: 0.9rem !important;
    box-shadow: 0 0 12px {GREEN}44 !important;
    transition: all 0.2s !important;
    width: 100% !important;
}}
.main-btn .stButton > button:hover {{
    box-shadow: 0 0 22px {GREEN}77 !important;
    transform: translateY(-1px) !important;
}}

/* ── Quiz cards ──────────────────────────────── */
.qcard {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 18px 20px;
    transition: border-color 0.2s, box-shadow 0.2s;
    margin-bottom: 12px;
}}
.qcard:hover {{ border-color: {GREEN}44; box-shadow: 0 4px 20px #00000055; }}
.diff-badge {{
    display: inline-block; border-radius: 20px;
    padding: 2px 9px; font-size: 0.7rem; font-weight: 700; margin-right: 6px;
}}
.xp {{ display: inline-block; background: #1b2b1b;
    border: 1px solid {GREEN}44; color: {GREEN};
    border-radius: 20px; padding: 2px 9px; font-size: 0.7rem; font-weight: 600; }}

.score-box {{
    background: {BG2}; border-radius: 14px;
    padding: 20px; text-align: center; margin: 12px 0;
}}

/* ── Auth screen — STAR.AI splash style ──────── */
.auth-card {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 2rem 1.8rem;
    box-shadow: 0 8px 40px #00000077;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: {BG3}; border-radius: 10px; padding: 3px; gap: 3px;
    margin-bottom: 0.5rem;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent; color: {MUTED};
    border-radius: 8px; padding: 7px 18px;
    font-weight: 600; font-size: 0.85rem;
}}
.stTabs [aria-selected="true"] {{ background: {GREEN} !important; color: #000 !important; }}

/* Start Chatting / auth CTA — full-width green pill (type="primary" buttons) */
[data-testid="stBaseButton-primary"] {{
    background: linear-gradient(135deg, {GREEN} 0%, {GLOW} 100%) !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 24px !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    box-shadow: 0 0 28px {GREEN}44 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    margin-top: 0.5rem !important;
}}
[data-testid="stBaseButton-primary"]:hover {{
    box-shadow: 0 0 42px {GREEN}66 !important;
    transform: translateY(-2px) !important;
}}

input[type="text"], input[type="password"] {{
    background: {BG3} !important; border: 1px solid {BORDER} !important;
    color: {TEXT} !important; border-radius: 9px !important;
}}

.tag {{
    display: inline-block; background: #1b2b1b;
    border: 1px solid {GREEN}44; color: {GLOW};
    border-radius: 20px; padding: 3px 11px;
    font-size: 0.72rem; margin: 3px; font-weight: 600;
}}

.stat-card {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 16px; text-align: center;
}}

.img-chip {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {BG2}; border: 1px solid {GREEN}44;
    border-radius: 10px; padding: 4px 10px;
    font-size: 0.78rem; color: {GREEN};
    margin-bottom: 8px; max-width: 760px; margin-left: auto;
    margin-right: auto;
}}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_client():
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        secret_key = ""
    key = (
        st.session_state.get("api_key")
        or os.getenv("OPENAI_API_KEY")
        or secret_key
    )
    return OpenAI(api_key=key) if key else None

def image_to_b64(image: Image.Image) -> tuple:
    buf = io.BytesIO()
    fmt = image.format or "JPEG"
    if fmt not in ("JPEG","PNG","WEBP"): fmt = "JPEG"
    image.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode(), fmt.lower()

def logo_b64():
    if os.path.exists("assets/logo.png"):
        with open("assets/logo.png","rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def logo_img_tag(size=56, radius=14, border=2):
    b64 = logo_b64()
    if b64:
        return f'<img src="data:image/png;base64,{b64}" style="width:{size}px;height:{size}px;border-radius:{radius}px;border:{border}px solid {GREEN};padding:4px;background:#111;">'
    return f'<div style="background:{GREEN};color:#000;font-weight:900;font-size:0.85rem;width:{size}px;height:{size}px;border-radius:{radius}px;display:inline-flex;align-items:center;justify-content:center;">PPI</div>'


# ── Prompts ───────────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """
You are PixelPulse AI, a friendly expert photography coach.
Analyse the image and reply in this exact format. Keep each section SHORT and punchy (2-4 bullets max). Simple language for beginners.

## ✨ Shot Summary
One sentence on what makes this shot work.

## 🔆 Lighting
- Type & direction
- Quality: hard / soft / diffused
- Mood it creates

## 📷 Camera Settings (estimated)
- **Aperture:** f/X — [effect]
- **Shutter:** 1/Xs
- **ISO:** X
- **Focal Length:** Xmm

## 💡 How to Recreate
3 clear beginner steps.

## 🏆 Pro Tip
One technique. One mistake to avoid.

## 🎓 Learn More
2 course picks:
- **[Platform] Name** — why · Free / ~$X

Under 350 words. End with one motivating line.
"""

def analyse_photo(client, image, extra=""):
    b64, fmt = image_to_b64(image)
    prompt = ANALYSIS_PROMPT + (f"\n\nUser note: {extra.strip()}" if extra.strip() else "")
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":[
            {"type":"text","text":prompt},
            {"type":"image_url","image_url":{"url":f"data:image/{fmt};base64,{b64}","detail":"high"}},
        ]}], max_tokens=700)
    return r.choices[0].message.content

def build_quiz_prompt(ch):
    reqs = "\n".join(f"- {r}" for r in ch["requirements"])
    return f"""
You are evaluating a photography challenge submission.

Challenge: {ch['title']} ({ch['difficulty']})
{ch['description']}

Requirements:
{reqs}

Context: {ch['eval_context']}

Respond in EXACTLY this format:

SCORE: [1-10]
PASSED: [Yes / No — Yes if score >= 6]
REQUIREMENTS:
{chr(10).join(f"- {r}: [✓ Met / ✗ Not met — one short reason]" for r in ch['requirements'])}
FEEDBACK: [2-3 specific sentences referencing what you see]
NEXT STEP: [one actionable improvement tip]
"""

def evaluate_submission(client, image, ch):
    b64, fmt = image_to_b64(image)
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":[
            {"type":"text","text":build_quiz_prompt(ch)},
            {"type":"image_url","image_url":{"url":f"data:image/{fmt};base64,{b64}","detail":"high"}},
        ]}], max_tokens=500)
    return r.choices[0].message.content

def parse_score(result):
    score, passed = 0, False
    for line in result.splitlines():
        if line.startswith("SCORE:"):
            try: score = int(line.split(":")[1].strip().split("/")[0])
            except: pass
        if line.startswith("PASSED:"):
            passed = "yes" in line.lower()
    return score, passed


# ── Session state ─────────────────────────────────────────────────────────────
defaults = dict(user_id=None, username=None, page="chat",
                current_session_id=None, messages=[],
                active_challenge=None, quiz_result=None,
                pending_image=None)
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════════════════════════════
#  AUTH SCREEN  —  STAR.AI splash style
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.user_id is None:
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        # Splash — logo with green radial glow
        b64 = logo_b64()
        if b64:
            logo_html = (
                f'<img src="data:image/png;base64,{b64}" '
                f'style="width:96px;height:96px;border-radius:24px;'
                f'border:2px solid {GREEN}88;padding:6px;background:#111;'
                f'box-shadow:0 0 44px {GREEN}55, 0 0 88px {GREEN}1a;'
                f'display:block;margin:0 auto;">'
            )
        else:
            logo_html = (
                f'<div style="width:96px;height:96px;border-radius:24px;'
                f'background:{GREEN};color:#000;font-weight:900;font-size:1.6rem;'
                f'display:inline-flex;align-items:center;justify-content:center;'
                f'margin:0 auto;box-shadow:0 0 44px {GREEN}55;">📷</div>'
            )

        st.markdown(f"""
        <div style="position:relative;text-align:center;padding:3.5rem 0 2.2rem 0;overflow:hidden;">
          <div style="position:absolute;top:42%;left:50%;transform:translate(-50%,-50%);
                      width:280px;height:280px;
                      background:radial-gradient(circle, {GREEN}1e 0%, {GREEN}09 45%, transparent 70%);
                      border-radius:50%;pointer-events:none;"></div>
          <div style="position:relative;z-index:1;margin-bottom:1.3rem;">{logo_html}</div>
          <div style="position:relative;z-index:1;font-size:2.1rem;font-weight:900;
                      color:{GREEN};letter-spacing:1.5px;line-height:1.1;">
            PixelPulse AI
          </div>
          <div style="position:relative;z-index:1;font-size:0.82rem;color:{MUTED};
                      margin-top:7px;letter-spacing:0.4px;">
            Your AI Photography Coach
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Login / Register form card
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        t_login, t_reg = st.tabs(["Login", "Create Account"])

        with t_login:
            u  = st.text_input("Username", placeholder="your username", key="li_u")
            p  = st.text_input("Password", type="password", placeholder="••••••••", key="li_p")
            if st.button("Start Chatting →", key="btn_li", type="primary", use_container_width=True):
                if u and p:
                    uid = db.login_user(u, p)
                    if uid:
                        st.session_state.user_id  = uid
                        st.session_state.username = u.lower().strip()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.warning("Please fill in both fields.")

        with t_reg:
            nu  = st.text_input("Username",         placeholder="choose a username", key="reg_u")
            np  = st.text_input("Password",         type="password", placeholder="min 6 chars",     key="reg_p")
            np2 = st.text_input("Confirm Password", type="password", placeholder="repeat password", key="reg_p2")
            if st.button("Create Account →", key="btn_reg", type="primary", use_container_width=True):
                if np != np2:  st.error("Passwords do not match.")
                elif nu and np:
                    ok, msg = db.register_user(nu, np)
                    st.success(msg) if ok else st.error(msg)
                else:          st.warning("Please fill all fields.")

        st.markdown('</div>', unsafe_allow_html=True)   # auth-card
    st.stop()


# ════════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
      {logo_img_tag(56, 14, 2)}
      <div class="sb-name">PixelPulse Innovation AI</div>
      <div class="sb-tagline">Photography Coach</div>
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio("", ["💬  Chat", "🏆  Quiz", "📊  Stats"],
                   key="nav_radio", label_visibility="collapsed")
    page_map = {"💬  Chat": "chat", "🏆  Quiz": "quiz", "📊  Stats": "stats"}
    st.session_state.page = page_map[nav]

    st.markdown("---")

    if st.session_state.page == "chat":
        st.markdown(f"<div style='font-size:0.8rem;font-weight:700;color:{MUTED};padding:0 4px 6px 4px;'>CHAT HISTORY</div>", unsafe_allow_html=True)
        if st.button("＋  New Chat", key="new_chat"):
            st.session_state.current_session_id = None
            st.session_state.messages = []
            st.rerun()

        sessions = db.get_sessions(st.session_state.user_id)
        for sid, title, created in sessions:
            active = st.session_state.current_session_id == sid
            css = "sess-item sess-active" if active else "sess-item"
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f'<div class="{css}">{title[:30]}</div>', unsafe_allow_html=True)
                if st.button("↩", key=f"load_{sid}", help="Load session"):
                    msgs = db.get_messages(sid)
                    st.session_state.current_session_id = sid
                    st.session_state.messages = [
                        {"role": r, "content": c, "image_b64": i} for r, c, i in msgs
                    ]
                    st.rerun()
            with c2:
                if st.button("✕", key=f"del_{sid}"):
                    db.delete_session(sid, st.session_state.user_id)
                    if st.session_state.current_session_id == sid:
                        st.session_state.current_session_id = None
                        st.session_state.messages = []
                    st.rerun()
        st.markdown("---")

    with st.expander("⚙️  API Key", expanded=not bool(get_client())):
        k = st.text_input("OpenAI Key", type="password", placeholder="sk-...", key="api_key")
        if k:
            st.session_state["api_key"] = k
            st.success("Saved ✓")

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.82rem;color:{MUTED};padding:2px 4px;'>👤 {st.session_state.username}</div>", unsafe_allow_html=True)
    if st.button("🚪  Logout"):
        for key in defaults: st.session_state[key] = defaults[key]
        st.rerun()
    st.markdown(f"<div style='font-size:0.65rem;color:#2a2a2a;text-align:center;padding-top:8px;'>PixelPulse Innovation AI</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  CHAT PAGE
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "chat":
    if st.session_state.messages:
        # Active chat — clean message list, no header clutter
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                if msg.get("image_b64"):
                    try:
                        img = db.b64_to_image(msg["image_b64"])
                        c1, c2 = st.columns([3, 1])
                        with c2: st.image(img, use_container_width=True)
                    except: pass
                st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-row"><span class="ai-avatar">AI</span><div class="bubble-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        # Empty state — STAR.AI style greeting + suggestion cards
        username    = st.session_state.username or "there"
        first_name  = username.split("_")[0].split(".")[0].title()
        avatar_init = first_name[0].upper() if first_name else "U"

        st.markdown(f"""
        <div class="greeting-header">
          <div class="greeting-top-bar">
            <div class="premium-badge">✨ Premium</div>
            <div class="user-avatar">{avatar_init}</div>
          </div>
          <div class="greeting-name">Hi {first_name},</div>
          <div class="greeting-sub">Give me any command, from analysing your shots<br>to coaching you through photography challenges</div>
        </div>
        """, unsafe_allow_html=True)

        # Suggestion cards — 2 × 2 grid
        suggestions = [
            ("📷", "Analyse the lighting and composition in my portrait shot"),
            ("✉️", "Help me understand camera settings for golden hour photography"),
            ("💬", "What's the most important skill for beginner photographers?"),
            ("🏆", "Give me a fun beginner photography challenge to try today"),
        ]

        st.markdown("<div style='padding:1.2rem 0 8rem 0;'>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="medium")
        for i, (icon, text) in enumerate(suggestions):
            with (col_a if i % 2 == 0 else col_b):
                st.markdown('<div class="suggest-btn">', unsafe_allow_html=True)
                if st.button(f"{icon}  {text}", key=f"sug_{i}"):
                    st.session_state["chat_text"] = text
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Input bar (fixed bottom) ──────────────────────────────────────────────
    if st.session_state.pending_image:
        st.markdown(f"""
        <div style="max-width:760px;margin:0 auto 4px auto;">
          <div class="img-chip">📎 {st.session_state.pending_image['name']} &nbsp;
            <span style="color:{MUTED};font-size:0.7rem;">ready to send</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="input-wrap"><div class="input-inner">', unsafe_allow_html=True)

    col_up, col_txt, col_send = st.columns([1, 14, 1])

    with col_up:
        st.markdown('<div class="upload-icon-wrap">', unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"],
                                    key="chat_file", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        if uploaded:
            img = Image.open(uploaded)
            st.session_state.pending_image = {
                "name": uploaded.name,
                "image": img,
                "b64": db.compress_image_b64(img)
            }

    with col_txt:
        st.markdown('<div class="text-wrap">', unsafe_allow_html=True)
        user_text = st.text_area("", placeholder="Tell me anything…",
                                 height=46, key="chat_text",
                                 label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_send:
        has_content = bool(user_text.strip()) or bool(st.session_state.pending_image)
        st.markdown('<div class="send-wrap">', unsafe_allow_html=True)
        send = st.button("↑", disabled=not has_content, key="send_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Send handler ──────────────────────────────────────────────────────────
    if send and has_content:
        client = get_client()
        if not client:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            img_data = st.session_state.pending_image
            image    = img_data["image"] if img_data else None
            img_b64  = img_data["b64"]   if img_data else None
            text     = user_text.strip() or "Analyse this photo."

            if st.session_state.current_session_id is None:
                title = (img_data["name"].rsplit(".",1)[0][:40] if img_data else text[:40]) or "Chat"
                sid   = db.create_session(st.session_state.user_id, title)
                st.session_state.current_session_id = sid

            db.add_message(st.session_state.current_session_id, "user", text, img_b64)
            st.session_state.messages.append({"role":"user","content":text,"image_b64":img_b64})

            with st.spinner("Thinking…"):
                try:
                    if image:
                        result = analyse_photo(client, image, text if text != "Analyse this photo." else "")
                    else:
                        r = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role":"system","content":"You are PixelPulse AI, a friendly photography coach. Answer concisely."},
                                {"role":"user","content":text}
                            ], max_tokens=500)
                        result = r.choices[0].message.content
                    db.add_message(st.session_state.current_session_id, "assistant", result)
                    st.session_state.messages.append({"role":"assistant","content":result,"image_b64":None})
                except Exception as e:
                    err = f"Error: {e}"
                    st.session_state.messages.append({"role":"assistant","content":err,"image_b64":None})

            st.session_state.pending_image = None
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
#  QUIZ PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "quiz":
    if st.session_state.active_challenge:
        ch = st.session_state.active_challenge
        dc = DIFFICULTY_COLOR.get(ch["difficulty"], GREEN)

        st.markdown(f"""
        <div style="margin-bottom:1.2rem;">
          <span style="font-size:2rem;">{ch['emoji']}</span>
          <span style="font-size:1.3rem;font-weight:800;margin-left:10px;">{ch['title']}</span>
          <span class="diff-badge" style="background:{dc}22;color:{dc};border:1px solid {dc}44;margin-left:10px;">{ch['difficulty']}</span>
          <span class="xp">+{ch['xp']} XP</span>
        </div>
        """, unsafe_allow_html=True)

        col_l, col_r = st.columns([1,1], gap="large")
        with col_l:
            st.markdown(f"**📋 Task**\n\n{ch['description']}")
            st.markdown("**✅ Requirements**")
            for r in ch["requirements"]:
                st.markdown(f"- {r}")
            st.info(f"💡 **Tip:** {ch['tip']}")
        with col_r:
            st.markdown("**📤 Upload Your Attempt**")
            qf = st.file_uploader("Drop your photo here",
                                   type=["jpg","jpeg","png","webp"],
                                   key=f"qf_{ch['id']}")
            if qf:
                st.image(qf, use_container_width=True)
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            sub_btn = st.button("Submit for Evaluation →", disabled=qf is None, key="sub_q")
            st.markdown('</div>', unsafe_allow_html=True)

            if sub_btn and qf:
                client = get_client()
                if not client:
                    st.error("Please enter your OpenAI API key in the sidebar.")
                else:
                    with st.spinner("Evaluating…"):
                        try:
                            img    = Image.open(qf)
                            result = evaluate_submission(client, img, ch)
                            score, passed = parse_score(result)
                            db.save_quiz_attempt(st.session_state.user_id, ch["title"],
                                                 ch["difficulty"], score, result, passed)
                            st.session_state.quiz_result = {"result":result,"score":score,"passed":passed}
                        except Exception as e:
                            st.error(f"Evaluation failed: {e}")

        if st.session_state.quiz_result:
            r  = st.session_state.quiz_result
            sc = GREEN if r["passed"] else "#e74c3c"
            lbl = "PASSED ✓" if r["passed"] else "NOT YET ✗"
            st.markdown(f"""
            <div class="score-box" style="border:2px solid {sc};box-shadow:0 0 24px {sc}33;">
              <div style="font-size:2.8rem;font-weight:800;color:{sc};">{r['score']}/10</div>
              <div style="color:{sc};font-weight:700;margin-top:4px;">{lbl}</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("📝 Full Evaluation", expanded=True):
                st.markdown(r["result"])

        if st.button("← Back to Challenges", key="back"):
            st.session_state.active_challenge = None
            st.session_state.quiz_result      = None
            st.rerun()
    else:
        st.markdown("#### 🏆 Photography Challenges")
        st.markdown(f"<small style='color:{MUTED}'>Upload your attempt and get AI feedback scored out of 10.</small>", unsafe_allow_html=True)
        st.markdown("")

        diff     = st.segmented_control("Difficulty", ["All","Beginner","Intermediate","Advanced"], default="All")
        filtered = CHALLENGES if diff == "All" else [c for c in CHALLENGES if c["difficulty"] == diff]

        c1, c2 = st.columns(2, gap="medium")
        for i, ch in enumerate(filtered):
            dc = DIFFICULTY_COLOR.get(ch["difficulty"], GREEN)
            with (c1 if i%2==0 else c2):
                st.markdown(f"""
                <div class="qcard">
                  <div style="font-size:1rem;font-weight:700;">{ch['emoji']} {ch['title']}</div>
                  <div style="margin:5px 0 8px 0;">
                    <span class="diff-badge" style="background:{dc}22;color:{dc};border:1px solid {dc}44;">{ch['difficulty']}</span>
                    <span style="color:{MUTED};font-size:0.75rem;">{ch['category']}</span>
                    <span class="xp" style="float:right;">+{ch['xp']} XP</span>
                  </div>
                  <div style="font-size:0.82rem;color:#888;line-height:1.5;">{ch['description'][:100]}…</div>
                </div>""", unsafe_allow_html=True)
                st.markdown('<div class="main-btn">', unsafe_allow_html=True)
                if st.button("Start Challenge →", key=f"start_{ch['id']}"):
                    st.session_state.active_challenge = ch
                    st.session_state.quiz_result      = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  STATS PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "stats":
    st.markdown(f"#### 📊 {st.session_state.username}'s Progress")
    stats   = db.get_quiz_stats(st.session_state.user_id)
    history = db.get_quiz_history(st.session_state.user_id)
    total_xp = sum(ch["xp"] for a in history for ch in CHALLENGES
                   if ch["title"] == a[0] and a[3])

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color in [
        (c1, "Attempted",  stats["total"],            TEXT),
        (c2, "Passed",     stats["passed"],            GREEN),
        (c3, "Avg Score",  f"{stats['avg_score']}/10", GREEN),
        (c4, "XP Earned",  f"{total_xp}",             GREEN),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div style="font-size:1.8rem;font-weight:800;color:{color};">{val}</div>
              <div style="font-size:0.73rem;color:{MUTED};margin-top:4px;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    sessions = db.get_sessions(st.session_state.user_id)
    st.markdown(f"**💬 Chat Sessions:** {len(sessions)}")
    st.markdown("---")

    if history:
        st.markdown("**📜 Quiz History**")
        for title, diff, score, passed, created in history:
            dc   = DIFFICULTY_COLOR.get(diff, GREEN)
            sc   = GREEN if passed else "#e74c3c"
            icon = "✅" if passed else "❌"
            st.markdown(f"""
            <div style="background:{BG2};border:1px solid {BORDER};border-radius:10px;
                        padding:11px 16px;margin:5px 0;
                        display:flex;align-items:center;justify-content:space-between;">
              <div>
                <span style="font-weight:700;">{icon} {title}</span>
                <span class="diff-badge" style="background:{dc}22;color:{dc};
                      border:1px solid {dc}44;margin-left:8px;">{diff}</span>
              </div>
              <div style="text-align:right;">
                <span style="font-size:1.1rem;font-weight:800;color:{sc};">{score}/10</span>
                <div style="font-size:0.68rem;color:{MUTED};">{created[:10]}</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:2rem;color:#333;">
          <div style="font-size:2.5rem;">🏆</div>
          <div style="margin-top:8px;color:#444;">No quiz attempts yet — head to Quiz Challenges!</div>
        </div>""", unsafe_allow_html=True)
