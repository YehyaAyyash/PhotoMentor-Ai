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

# ── Brand colours ─────────────────────────────────────────────────────────────
GREEN  = "#8FD14F"
GLOW   = "#a3e063"
BG     = "#0d0d0d"
BG2    = "#141414"
BG3    = "#1a1a1a"
BORDER = "#222222"
TEXT   = "#e4e4e4"
MUTED  = "#555555"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

  html, body, .stApp {{
      background-color: {BG};
      color: {TEXT};
      font-family: 'Inter', sans-serif;
  }}
  ::-webkit-scrollbar {{ width: 5px; }}
  ::-webkit-scrollbar-track {{ background: {BG}; }}
  ::-webkit-scrollbar-thumb {{ background: {GREEN}; border-radius: 4px; }}

  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 0.8rem !important; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{ background: {BG3} !important; border-right: 1px solid {BORDER}; }}
  [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

  /* Auth card */
  .auth-card {{
      background: {BG2};
      border: 1px solid {BORDER};
      border-radius: 16px;
      padding: 2.5rem 2rem;
      max-width: 420px;
      margin: 3rem auto;
      box-shadow: 0 8px 32px #00000055;
  }}
  .auth-logo {{
      text-align: center;
      margin-bottom: 1.5rem;
  }}
  .auth-logo img {{
      height: 64px; width: 64px;
      border-radius: 14px;
      border: 2px solid {GREEN};
      padding: 5px; background: #111;
  }}
  .auth-title {{
      font-size: 1.4rem; font-weight: 800;
      color: {GREEN}; text-align: center;
      margin-bottom: 0.2rem;
  }}
  .auth-sub {{
      color: {MUTED}; font-size: 0.8rem;
      text-align: center; margin-bottom: 1.5rem;
  }}

  /* Brand header */
  .brand-header {{
      display: flex; align-items: center;
      gap: 12px; padding: 0.8rem 0 0.3rem 0;
  }}
  .brand-header img {{
      height: 46px; width: 46px; object-fit: contain;
      border-radius: 10px; border: 1.5px solid {GREEN};
      padding: 3px; background: #111;
  }}
  .brand-title {{ font-size: 1.4rem; font-weight: 800; color: {GREEN}; line-height: 1.1; }}
  .brand-sub   {{ font-size: 0.7rem; color: {MUTED}; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {{ background: {BG2}; border-radius: 10px; padding: 4px; gap: 4px; }}
  .stTabs [data-baseweb="tab"] {{
      background: transparent; color: {MUTED};
      border-radius: 8px; padding: 8px 20px;
      font-weight: 600; font-size: 0.88rem;
  }}
  .stTabs [aria-selected="true"] {{ background: {GREEN} !important; color: #000 !important; }}

  /* Chat bubbles */
  .bubble-user {{
      background: #1b2b1b; border: 1px solid {GREEN}33;
      border-radius: 16px 16px 4px 16px;
      padding: 11px 15px; margin: 8px 0 8px auto;
      max-width: 80%; color: {TEXT}; font-size: 0.87rem;
  }}
  .bubble-ai {{
      background: {BG2}; border-left: 3px solid {GREEN};
      border-radius: 4px 16px 16px 16px;
      padding: 13px 17px; margin: 6px 0;
      max-width: 96%; color: {TEXT}; font-size: 0.87rem;
      line-height: 1.65; box-shadow: 0 2px 12px #00000033;
  }}
  .bubble-ai h2 {{
      font-size: 0.82rem; font-weight: 700; color: {GREEN};
      margin: 12px 0 4px 0; border-bottom: 1px solid {BORDER};
      padding-bottom: 3px; text-transform: uppercase; letter-spacing: 0.4px;
  }}
  .bubble-ai ul {{ padding-left: 16px; margin: 4px 0 8px 0; }}
  .bubble-ai li {{ margin-bottom: 4px; }}
  .bubble-ai strong {{ color: {GLOW}; }}
  .avatar {{ display:inline-flex; align-items:center; justify-content:center;
      background:{GREEN}; color:#000; font-weight:800; font-size:0.65rem;
      border-radius:50%; width:24px; height:24px; flex-shrink:0; margin-right:6px; }}
  .msg-row {{ display:flex; align-items:flex-start; gap:6px; margin:6px 0; }}

  /* Session items in sidebar */
  .session-item {{
      background: {BG2}; border: 1px solid {BORDER};
      border-radius: 8px; padding: 8px 10px; margin: 4px 0;
      cursor: pointer; font-size: 0.82rem; color: {TEXT};
      transition: border-color 0.2s;
  }}
  .session-item:hover {{ border-color: {GREEN}; }}
  .session-active {{ border-color: {GREEN} !important; background: #1b2b1b !important; }}

  /* Quiz cards */
  .quiz-card {{
      background: {BG2}; border: 1px solid {BORDER};
      border-radius: 14px; padding: 18px 20px; margin-bottom: 14px;
      transition: border-color 0.2s, box-shadow 0.2s;
  }}
  .quiz-card:hover {{ border-color: {GREEN}55; box-shadow: 0 4px 20px #00000044; }}
  .quiz-card-title {{ font-size: 1rem; font-weight: 700; color: {TEXT}; }}
  .quiz-card-meta  {{ font-size: 0.75rem; color: {MUTED}; margin: 4px 0 8px 0; }}
  .quiz-card-desc  {{ font-size: 0.83rem; color: #aaa; line-height: 1.5; }}
  .diff-badge {{
      display: inline-block; border-radius: 20px;
      padding: 2px 10px; font-size: 0.72rem; font-weight: 700;
      margin-right: 6px;
  }}
  .xp-badge {{
      display: inline-block; background: #1b2b1b;
      border: 1px solid {GREEN}44; color: {GREEN};
      border-radius: 20px; padding: 2px 10px;
      font-size: 0.72rem; font-weight: 600;
  }}

  /* Score display */
  .score-box {{
      background: {BG2}; border: 2px solid {GREEN};
      border-radius: 14px; padding: 20px 24px; text-align: center;
      margin: 12px 0; box-shadow: 0 0 24px {GREEN}33;
  }}
  .score-num {{ font-size: 3rem; font-weight: 800; color: {GREEN}; line-height: 1; }}
  .score-label {{ font-size: 0.8rem; color: {MUTED}; margin-top: 4px; }}

  /* Tag */
  .tag {{
      display: inline-block; background: #1b2b1b;
      border: 1px solid {GREEN}55; color: {GLOW};
      border-radius: 20px; padding: 3px 11px;
      font-size: 0.73rem; margin: 3px 3px; font-weight: 600;
  }}

  /* Buttons */
  .stButton > button {{
      background: linear-gradient(135deg, {GREEN}, {GLOW});
      color: #000 !important; font-weight: 700;
      border: none; border-radius: 8px; width: 100%;
      padding: 10px; font-size: 0.9rem;
      box-shadow: 0 0 12px {GREEN}44;
      transition: all 0.2s;
  }}
  .stButton > button:hover {{
      box-shadow: 0 0 22px {GREEN}88;
      transform: translateY(-1px);
  }}
  .stButton > button:disabled {{ opacity: 0.3; box-shadow: none; transform: none; }}

  /* Inputs */
  [data-testid="stFileUploader"] {{
      background: {BG3}; border: 1.5px dashed {GREEN}44;
      border-radius: 10px; padding: 8px;
  }}
  textarea, input[type="text"], input[type="password"] {{
      background: {BG3} !important; border: 1px solid {BORDER} !important;
      color: {TEXT} !important; border-radius: 8px !important;
  }}
  .stSpinner > div {{ border-top-color: {GREEN} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_client():
    key = (
        st.session_state.get("api_key")
        or os.getenv("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY", "")
    )
    return OpenAI(api_key=key) if key else None

def image_to_b64(image: Image.Image) -> tuple:
    buf = io.BytesIO()
    fmt = image.format or "JPEG"
    if fmt not in ("JPEG", "PNG", "WEBP"):
        fmt = "JPEG"
    image.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode(), fmt.lower()

def logo_b64():
    path = "assets/logo.png"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def render_logo_header(subtitle="Photography Coaching · GPT-4o Mini"):
    b64 = logo_b64()
    if b64:
        st.markdown(f"""
        <div class="brand-header">
          <img src="data:image/png;base64,{b64}">
          <div>
            <div class="brand-title">PixelPulse Innovation AI</div>
            <div class="brand-sub">{subtitle}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="brand-header">
          <div style="background:{GREEN};color:#000;font-weight:900;font-size:0.9rem;
                      width:46px;height:46px;border-radius:10px;display:flex;
                      align-items:center;justify-content:center;">PPI</div>
          <div>
            <div class="brand-title">PixelPulse Innovation AI</div>
            <div class="brand-sub">{subtitle}</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ── Analysis prompt ───────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """
You are PixelPulse AI, a friendly photography coach. Analyse the image and reply in this exact format.
Keep each section SHORT (2-4 bullet points max). Use simple language for beginners.

## ✨ Shot Summary
One sentence: what makes this shot stand out.

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
3 clear steps for a beginner.

## 🏆 Pro Tip
One technique used. One mistake to avoid.

## 🎓 Learn More
2 relevant course picks:
- **[Platform] Course Name** — why · Free / ~$X

Under 350 words. End with one motivating line.
"""

def analyse_photo(client, image: Image.Image, extra: str = "") -> str:
    b64, fmt = image_to_b64(image)
    prompt = ANALYSIS_PROMPT + (f"\n\nUser note: {extra.strip()}" if extra.strip() else "")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{fmt};base64,{b64}", "detail": "high"}},
        ]}],
        max_tokens=700,
    )
    return resp.choices[0].message.content


# ── Quiz evaluation prompt ────────────────────────────────────────────────────
def build_quiz_prompt(challenge: dict) -> str:
    reqs = "\n".join(f"- {r}" for r in challenge["requirements"])
    return f"""
You are evaluating a photography challenge submission for PixelPulse Innovation AI.

Challenge: {challenge['title']}
Difficulty: {challenge['difficulty']}
Description: {challenge['description']}

Requirements to check:
{reqs}

Additional context: {challenge['eval_context']}

Carefully examine the uploaded photo and respond in EXACTLY this format:

SCORE: [number 1-10]
PASSED: [Yes / No — Yes if score >= 6]
REQUIREMENTS:
{chr(10).join(f"- {r}: [✓ Met / ✗ Not met — one short reason]" for r in challenge['requirements'])}
FEEDBACK: [2-3 sentences of specific, constructive feedback referencing what you see in the photo]
NEXT STEP: [One specific actionable tip to improve this type of shot]
"""

def evaluate_submission(client, image: Image.Image, challenge: dict) -> str:
    b64, fmt = image_to_b64(image)
    prompt = build_quiz_prompt(challenge)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/{fmt};base64,{b64}", "detail": "high"}},
        ]}],
        max_tokens=500,
    )
    return resp.choices[0].message.content

def parse_score(result: str) -> tuple:
    score, passed = 0, False
    for line in result.splitlines():
        if line.startswith("SCORE:"):
            try: score = int(line.split(":")[1].strip().split("/")[0])
            except: pass
        if line.startswith("PASSED:"):
            passed = "yes" in line.lower()
    return score, passed


# ── Session state init ────────────────────────────────────────────────────────
for key, val in {
    "user_id": None, "username": None,
    "auth_tab": "login",
    "current_session_id": None,
    "messages": [],
    "active_challenge": None,
    "quiz_result": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ════════════════════════════════════════════════════════════════════════════════
#  AUTH SCREEN
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.user_id is None:
    b64 = logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{b64}">'
        if b64 else
        f'<div style="background:{GREEN};color:#000;font-weight:900;font-size:1.2rem;'
        f'width:64px;height:64px;border-radius:14px;display:inline-flex;'
        f'align-items:center;justify-content:center;">PPI</div>'
    )
    st.markdown(f"""
    <div class="auth-card">
      <div class="auth-logo">{logo_html}</div>
      <div class="auth-title">PixelPulse Innovation AI</div>
      <div class="auth-sub">Your AI photography coach</div>
    </div>
    """, unsafe_allow_html=True)

    # Centre the auth card
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        tab_login, tab_register = st.tabs(["Login", "Create Account"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            uname = st.text_input("Username", key="login_user", placeholder="your username")
            pwd   = st.text_input("Password", key="login_pass", type="password", placeholder="••••••••")
            if st.button("Login", key="btn_login"):
                if uname and pwd:
                    uid = db.login_user(uname, pwd)
                    if uid:
                        st.session_state.user_id  = uid
                        st.session_state.username = uname.lower().strip()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.warning("Please fill in both fields.")

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            new_u = st.text_input("Username", key="reg_user", placeholder="choose a username")
            new_p = st.text_input("Password", key="reg_pass", type="password", placeholder="min 6 characters")
            new_p2 = st.text_input("Confirm Password", key="reg_pass2", type="password", placeholder="repeat password")
            if st.button("Create Account", key="btn_register"):
                if new_p != new_p2:
                    st.error("Passwords do not match.")
                elif new_u and new_p:
                    ok, msg = db.register_user(new_u, new_p)
                    if ok:
                        st.success(f"{msg} Please login.")
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")
    st.stop()


# ════════════════════════════════════════════════════════════════════════════════
#  MAIN APP  (authenticated)
# ════════════════════════════════════════════════════════════════════════════════

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    b64 = logo_b64()
    if b64:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0 12px 0;">
          <img src="data:image/png;base64,{b64}"
               style="height:36px;width:36px;border-radius:8px;
                      border:1.5px solid {GREEN};padding:3px;background:#111;">
          <div>
            <div style="font-weight:800;color:{GREEN};font-size:0.9rem;line-height:1.1;">PixelPulse</div>
            <div style="font-size:0.65rem;color:{MUTED};text-transform:uppercase;letter-spacing:0.5px;">Innovation AI</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"**👤 {st.session_state.username}**")
    st.markdown("---")

    # API Key
    with st.expander("⚙️ API Key", expanded=not bool(get_client())):
        key_in = st.text_input("OpenAI API Key", type="password", placeholder="sk-...", key="api_key_input")
        if key_in:
            st.session_state["api_key"] = key_in
            st.success("Saved ✓")

    st.markdown("---")

    # Chat history
    st.markdown("**💬 Chat History**")
    if st.button("＋ New Chat", key="new_chat"):
        st.session_state.current_session_id = None
        st.session_state.messages = []
        st.rerun()

    sessions = db.get_sessions(st.session_state.user_id)
    for sid, title, created in sessions:
        is_active = st.session_state.current_session_id == sid
        css_class = "session-item session-active" if is_active else "session-item"
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(
                f'<div class="{css_class}" title="{created[:10]}">{title[:32]}</div>',
                unsafe_allow_html=True
            )
            if st.button("Load", key=f"load_{sid}", help=f"Open: {title}"):
                msgs = db.get_messages(sid)
                st.session_state.current_session_id = sid
                st.session_state.messages = [
                    {"role": r, "content": c, "image_b64": i}
                    for r, c, i in msgs
                ]
                st.rerun()
        with cols[1]:
            if st.button("🗑", key=f"del_{sid}", help="Delete"):
                db.delete_session(sid, st.session_state.user_id)
                if st.session_state.current_session_id == sid:
                    st.session_state.current_session_id = None
                    st.session_state.messages = []
                st.rerun()

    st.markdown("---")
    if st.button("🚪 Logout"):
        for k in ["user_id", "username", "current_session_id", "messages",
                  "active_challenge", "quiz_result"]:
            st.session_state[k] = None if k not in ["messages"] else []
        st.rerun()
    st.markdown("---")
    st.caption("PixelPulse Innovation AI · GPT-4o Mini")


# ── Header ────────────────────────────────────────────────────────────────────
render_logo_header()
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_chat, tab_quiz, tab_stats = st.tabs(["💬 Chat", "🏆 Quiz Challenges", "📊 My Stats"])


# ════════════════════════════════════════════════════════════════════════════════
#  CHAT TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_chat:
    # Render messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                if msg.get("image_b64"):
                    try:
                        img = db.b64_to_image(msg["image_b64"])
                        st.image(img, width=260)
                    except: pass
                st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-row">
                  <span class="avatar">AI</span>
                  <div class="bubble-ai">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:2.5rem 0 1rem 0;color:#333;">
          <div style="font-size:3rem;">📷</div>
          <div style="font-size:0.95rem;color:#444;margin-top:10px;">Upload a photo to get instant coaching</div>
          <div style="margin-top:14px;">
            <span class="tag">Lighting Analysis</span>
            <span class="tag">Camera Settings</span>
            <span class="tag">Recreation Guide</span>
            <span class="tag">Pro Tips</span>
            <span class="tag">Course Picks</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_f, col_c = st.columns([1, 1.5])
    with col_f:
        uploaded = st.file_uploader("Photo", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if uploaded:
            st.image(uploaded, width=220)
    with col_c:
        extra = st.text_area("Context (optional)", placeholder="e.g. 'indoor portrait at night'…",
                             height=82, label_visibility="collapsed")
        analyse_btn = st.button("📸 Analyse Photo", disabled=uploaded is None, key="analyse_btn")

    if analyse_btn and uploaded:
        client = get_client()
        if not client:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            image = Image.open(uploaded)
            img_b64_store = db.compress_image_b64(image)

            # Create session if needed
            if st.session_state.current_session_id is None:
                title = uploaded.name.replace("_", " ").rsplit(".", 1)[0][:40] or "Photo Analysis"
                sid = db.create_session(st.session_state.user_id, title)
                st.session_state.current_session_id = sid

            user_text = f"Analyse this photo{': ' + extra.strip() if extra.strip() else '.'}"
            db.add_message(st.session_state.current_session_id, "user", user_text, img_b64_store)
            st.session_state.messages.append({"role": "user", "content": user_text, "image_b64": img_b64_store})

            with st.spinner("Analysing your photo…"):
                try:
                    result = analyse_photo(client, image, extra)
                    db.add_message(st.session_state.current_session_id, "assistant", result)
                    st.session_state.messages.append({"role": "assistant", "content": result, "image_b64": None})
                except Exception as e:
                    err = f"Analysis failed: {e}"
                    st.session_state.messages.append({"role": "assistant", "content": err, "image_b64": None})
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
#  QUIZ TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_quiz:
    # ── Active challenge view ─────────────────────────────────────────────────
    if st.session_state.active_challenge:
        ch = st.session_state.active_challenge

        diff_color = DIFFICULTY_COLOR.get(ch["difficulty"], GREEN)
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
          <span style="font-size:2rem;">{ch['emoji']}</span>
          <span style="font-size:1.3rem;font-weight:800;color:{TEXT};margin-left:10px;">{ch['title']}</span>
          <span class="diff-badge" style="background:{diff_color}22;color:{diff_color};
                border:1px solid {diff_color}55;margin-left:10px;">{ch['difficulty']}</span>
          <span class="xp-badge">+{ch['xp']} XP</span>
        </div>
        """, unsafe_allow_html=True)

        col_desc, col_submit = st.columns([1, 1], gap="large")

        with col_desc:
            st.markdown(f"**📋 Challenge**\n\n{ch['description']}")
            st.markdown("**✅ Requirements**")
            for r in ch["requirements"]:
                st.markdown(f"- {r}")
            st.info(f"💡 **Tip:** {ch['tip']}")

        with col_submit:
            st.markdown("**📤 Submit Your Photo**")
            quiz_file = st.file_uploader("Upload your attempt",
                                          type=["jpg","jpeg","png","webp"],
                                          key=f"quiz_upload_{ch['id']}")
            if quiz_file:
                st.image(quiz_file, use_container_width=True)

            submit_btn = st.button("Submit for Evaluation", disabled=quiz_file is None, key="submit_quiz")

            if submit_btn and quiz_file:
                client = get_client()
                if not client:
                    st.error("Please enter your OpenAI API key in the sidebar.")
                else:
                    with st.spinner("Evaluating your submission…"):
                        try:
                            img = Image.open(quiz_file)
                            result = evaluate_submission(client, img, ch)
                            score, passed = parse_score(result)
                            db.save_quiz_attempt(
                                st.session_state.user_id,
                                ch["title"], ch["difficulty"],
                                score, result, passed
                            )
                            st.session_state.quiz_result = {"result": result, "score": score, "passed": passed}
                        except Exception as e:
                            st.error(f"Evaluation failed: {e}")

        # Result display
        if st.session_state.quiz_result:
            r = st.session_state.quiz_result
            status_color = GREEN if r["passed"] else "#e74c3c"
            status_label = "PASSED ✓" if r["passed"] else "NOT YET ✗"

            st.markdown(f"""
            <div class="score-box" style="border-color:{status_color};box-shadow:0 0 24px {status_color}33;">
              <div class="score-num" style="color:{status_color};">{r['score']}/10</div>
              <div class="score-label" style="color:{status_color};font-weight:700;">{status_label}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📝 View Full Evaluation", expanded=True):
                st.markdown(r["result"])

        col_back, _ = st.columns([1, 3])
        with col_back:
            if st.button("← Back to Challenges", key="back_challenges"):
                st.session_state.active_challenge = None
                st.session_state.quiz_result = None
                st.rerun()

    # ── Challenge grid ────────────────────────────────────────────────────────
    else:
        st.markdown("#### Pick a Challenge")
        st.markdown("<small style='color:#555;'>Complete challenges to sharpen your photography skills. "
                    "Upload your attempt and get AI feedback.</small>", unsafe_allow_html=True)
        st.markdown("")

        # Filter by difficulty
        diff_filter = st.segmented_control(
            "Difficulty", ["All", "Beginner", "Intermediate", "Advanced"],
            default="All", key="diff_filter"
        )

        filtered = CHALLENGES if diff_filter == "All" else [
            c for c in CHALLENGES if c["difficulty"] == diff_filter
        ]

        col1, col2 = st.columns(2, gap="medium")
        for i, ch in enumerate(filtered):
            diff_color = DIFFICULTY_COLOR.get(ch["difficulty"], GREEN)
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div class="quiz-card">
                  <div class="quiz-card-title">{ch['emoji']} {ch['title']}</div>
                  <div class="quiz-card-meta">
                    <span class="diff-badge" style="background:{diff_color}22;color:{diff_color};
                          border:1px solid {diff_color}44;">{ch['difficulty']}</span>
                    <span style="color:{MUTED};">{ch['category']}</span>
                    <span class="xp-badge" style="float:right;">+{ch['xp']} XP</span>
                  </div>
                  <div class="quiz-card-desc">{ch['description'][:100]}…</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Start Challenge", key=f"start_{ch['id']}"):
                    st.session_state.active_challenge = ch
                    st.session_state.quiz_result = None
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
#  STATS TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown(f"#### {st.session_state.username}'s Progress")

    stats = db.get_quiz_stats(st.session_state.user_id)
    total_xp = sum(
        ch["xp"] for a in db.get_quiz_history(st.session_state.user_id)
        for ch in CHALLENGES if ch["title"] == a[0] and a[3]
    )

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, color in [
        (c1, "Challenges Attempted", stats["total"], TEXT),
        (c2, "Challenges Passed",    stats["passed"], GREEN),
        (c3, "Average Score",        f"{stats['avg_score']}/10", GREEN),
        (c4, "Total XP Earned",      f"{total_xp} XP", GREEN),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:{BG2};border:1px solid {BORDER};border-radius:12px;
                        padding:16px;text-align:center;margin-bottom:10px;">
              <div style="font-size:1.8rem;font-weight:800;color:{color};">{value}</div>
              <div style="font-size:0.75rem;color:{MUTED};margin-top:4px;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    history = db.get_quiz_history(st.session_state.user_id)
    if history:
        st.markdown("**📜 Quiz History**")
        for title, diff, score, passed, created in history:
            diff_color = DIFFICULTY_COLOR.get(diff, GREEN)
            status_icon = "✅" if passed else "❌"
            score_color = GREEN if passed else "#e74c3c"
            st.markdown(f"""
            <div style="background:{BG2};border:1px solid {BORDER};border-radius:10px;
                        padding:12px 16px;margin:6px 0;display:flex;
                        align-items:center;justify-content:space-between;">
              <div>
                <span style="font-weight:700;color:{TEXT};">{status_icon} {title}</span>
                <span class="diff-badge" style="background:{diff_color}22;color:{diff_color};
                      border:1px solid {diff_color}44;margin-left:8px;">{diff}</span>
              </div>
              <div style="text-align:right;">
                <span style="font-size:1.1rem;font-weight:800;color:{score_color};">{score}/10</span>
                <div style="font-size:0.7rem;color:{MUTED};">{created[:10]}</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:2rem;color:#444;">
          <div style="font-size:2.5rem;">🏆</div>
          <div style="margin-top:8px;">No quiz attempts yet. Head to Quiz Challenges to get started!</div>
        </div>""", unsafe_allow_html=True)

    # Chat session stats
    sessions = db.get_sessions(st.session_state.user_id)
    st.markdown("---")
    st.markdown(f"**💬 Chat Sessions:** {len(sessions)} total")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<center><small style='color:#222;'>PixelPulse Innovation AI · Built by Yahya Ayyash</small></center>",
    unsafe_allow_html=True,
)
