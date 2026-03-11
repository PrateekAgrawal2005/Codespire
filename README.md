# 🤖 Codespire — AI Learning & Research Assistant

A sleek, AI-powered web app built with **Streamlit** and **Google Gemini**, designed to help students, developers, and curious minds get rich, detailed answers — from debugging code to building full learning roadmaps.

---

## ✨ Features

- **Multiple Gemini Models** — Switch between `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, and `gemini-2.5-pro` depending on speed vs. capability needs
- **Quick Start Templates** — One-click prompts for Study Plans, Career Guides, and Debug Help
- **Customizable System Prompt** — Edit the AI's behavior and personality directly in the sidebar
- **Response Length & Creativity Controls** — Sliders for length (Brief → Comprehensive) and temperature (Factual → Creative)
- **Dark Premium UI** — Gradient-rich, fully dark-themed interface built with custom CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| AI Backend | Google Gemini (via `google-genai`) |
| Environment | Python 3.10+, `python-dotenv` |
| Deployment | Streamlit Cloud / Local |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/SomyaKothari9906/Codespire.git
cd Codespire
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
Codespire/
├── app.py              # Main Streamlit application
├── .env                # API key (gitignored — never committed)
├── .env.example        # Template for environment variables
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignores .env, myenv/, __pycache__/
└── README.md           # You are here
```

---

## 🔐 Security

- The `.env` file is listed in `.gitignore` and is **never committed to GitHub**
- Use `.env.example` as a template — it contains no real credentials
- Never hard-code API keys in source files

---

## 👥 Contributors

- [Somya Kothari](https://github.com/SomyaKothari9906)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
