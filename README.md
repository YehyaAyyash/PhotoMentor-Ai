# 📷 PhotoMentor AI

> An AI-powered photography coaching chatbot that analyses any photo and teaches beginners how to master it.

![PhotoMentor AI](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=flat&logo=streamlit)
![GPT-4o Mini](https://img.shields.io/badge/Powered%20by-GPT--4o%20Mini-412991?style=flat&logo=openai)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python)

---

## ✨ What It Does

Upload any photo — AI-generated or real — and PhotoMentor instantly breaks it down for you:

| Feature | Description |
|---|---|
| 🔆 **Lighting Analysis** | Type, direction, quality, and mood of the light |
| 📷 **Camera Settings** | Estimated aperture, shutter speed, ISO, focal length |
| 💡 **Recreation Guide** | Step-by-step instructions to recreate the shot |
| 🏆 **Pro Tips** | Advanced techniques and beginner mistakes to avoid |
| 🎓 **Course Picks** | 2 curated courses matched to the photo style |

All responses are short, punchy, and beginner-friendly — delivered in a clean **chat interface**.

---

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://photomentor-ai.streamlit.app)

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io) — Python-based web UI
- **AI Vision:** [OpenAI GPT-4o Mini](https://platform.openai.com/docs/models/gpt-4o-mini) — image understanding & analysis
- **Language:** Python 3.9+

---

## ⚡ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YehyaAyyash/PhotoMentor-Ai.git
cd PhotoMentor-Ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your OpenAI API key**

Option A — `.env` file:
```bash
cp .env.example .env
# Edit .env and add your key:
# OPENAI_API_KEY=sk-...
```

Option B — paste the key directly in the app sidebar (no setup needed).

**4. Run**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

> **API Key:** Get one at [platform.openai.com](https://platform.openai.com) → API Keys → Create new secret key.
> **Cost:** ~$0.001 per analysis (very cheap).

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repo → set main file to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. Click **Deploy** — done!

---

## 📁 Project Structure

```
PhotoMentor-Ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── .gitignore
└── README.md
```

---

## 🔭 Future Ideas

### 🤖 AI Enhancements
- [ ] **Multi-turn chat** — ask follow-up questions about the same photo
- [ ] **Before/After comparison** — upload two photos and compare techniques
- [ ] **Style matching** — "make my photo look like this reference"
- [ ] **Gear recommender** — suggest specific camera/lens combos based on the shot

### 📚 Learning Features
- [ ] **Progress tracker** — save analyses and track skill improvement over time
- [ ] **Daily challenge** — upload a photo matching a given style prompt
- [ ] **Glossary mode** — tap any term (e.g. "Rembrandt lighting") for a quick explainer
- [ ] **Quiz mode** — test your knowledge based on analysed photos

### 🌐 Platform & UX
- [ ] **Mobile-optimised UI** — better camera upload flow on phones
- [ ] **Export to PDF** — save full analysis as a printable guide
- [ ] **Community gallery** — share and learn from other users' photos
- [ ] **Multi-language support** — coaching in Spanish, French, Arabic, etc.

### 🔗 Integrations
- [ ] **Instagram import** — analyse photos directly from a profile URL
- [ ] **Lightroom/Capture One presets** — auto-generate export presets based on analysis
- [ ] **YouTube** — match analysis to relevant tutorial timestamps

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/YehyaAyyash">Yahya Ayyash</a>
</div>
