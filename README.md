#  BMSCE AI Chatbot Assistant
> An intelligent, hybrid campus chatbot assistant for **BMS College of Engineering (BMSCE), Bangalore**. Features multi-tier knowledge retrieval, fuzzy keyword matching, contradiction resolution, live web search, and Gemini AI fallback.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Gemini_AI-2.0_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

##  Overview

The **BMSCE AI Chatbot** is designed to provide students, faculty, and prospective applicants with fast, reliable, and verified answers regarding BMS College of Engineering. 

Rather than relying purely on generative AI hallucinations, the assistant utilizes a **strict 4-tier answer hierarchy**:
1. **Tier 1 — Local/Supabase Knowledge Base**: High-confidence curated answers with verification sources.
2. **Tier 2 — Contradiction Engine**: Surfaces multiple perspectives on disputed or subjective topics (e.g. grading strictness, hostel reviews).
3. **Tier 3 — Live Web Search**: Scrapes official `bmsce.ac.in` and community forums using DuckDuckGo.
4. **Tier 4 — Gemini 2.0 Flash AI**: Synthesizes and answers queries when no exact knowledge base match exists.

---

##  Features

- ** Multi-Level Trust Scoring**:
  - `Official` (Green): Direct information from college administration and circulars.
  - `Verified` (Yellow): Fact-checked student data & guidelines.
  - `Student Opinion` (Red/Orange): Subjective community perspectives.
  - `Dynamic Web` (Purple): Live search results synthesized from official domain/web.
- ** Smart Fuzzy Matching**: Handles student typos (`attandance strict`, `canteen timmings`) seamlessly via `difflib` and keyword token scoring.
- ** Desktop-Optimized 3-Column UI**:
  - Left navigation & quick topic filters
  - Main interactive conversation feed
  - Right sidebar with campus widgets, shortcuts, and trust distribution meter
- **⌨️ Power-User Shortcuts**:
  - `Ctrl + K`: Quick focus chat bar
  - `Ctrl + N`: New chat session
  - `Ctrl + E`: Export conversation to `.txt`
  - `Ctrl + F`: In-chat message search
  - `Ctrl + Up / Down`: Cycle previous inputs

---

##  Architecture & Tech Stack

```
[ Browser UI (HTML5 / Vanilla CSS / JS) ]
                   │
                   ▼ HTTP REST
[ Flask Backend (`app.py`) + Gunicorn WSGI ]
   ├── 1. Knowledge Base (`knowledge_base.py` / Supabase REST API)
   ├── 2. Fuzzy Token Matcher & Stop-word Filter
   ├── 3. Contradiction Resolution Engine
   ├── 4. DuckDuckGo Scraper (`web_scraper.py`)
   └── 5. Google Gemini 2.0 Flash (`google-generativeai`)
```

- **Backend**: Python, Flask, Flask-CORS, Gunicorn
- **Frontend**: Responsive HTML5, Modern CSS Glassmorphism/Dark Theme, Vanilla JavaScript
- **Database / Cloud KB**: Supabase REST API (PostgreSQL)
- **AI & Search**: Google Gemini API (`gemini-2.0-flash`), DuckDuckGo Search API

---

##  Project Structure

```bash
BMSCE-Chatbox-Assistant/
├── .env.example             # Example environment variables
├── .gitignore               # Ignored files (secrets, caches, logs)
├── Procfile                 # Deployment process command for cloud hosts
├── requirements.txt         # Production Python packages
├── app.py                   # Main Flask server & routing engine
├── knowledge_base.py        # Curated BMSCE Q&A entries & contradiction sets
├── web_scraper.py           # DuckDuckGo fallback search & summarizer
├── setup_supabase.py        # Script to seed knowledge base into Supabase
├── setup_db.py              # SQLite migration helper
├── schema.sql               # Database schema definition
├── templates/
│   └── index.html           # Main chat web application interface
└── static/
    ├── style.css            # Custom responsive styles & animations
    └── script.js            # Chat interactions, shortcuts & storage logic
```

---

##  Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Harshita-Shreevastav/BMSCE-Chatbox-Assistant.git
cd BMSCE-Chatbox-Assistant
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SUPABASE_URL="https://your-supabase-project.supabase.co"
SUPABASE_KEY="your-supabase-anon-key"
GOOGLE_API_KEY="your-gemini-api-key"
```
*(Note: If no Gemini API key is provided, the chatbot seamlessly operates using the local curated knowledge base).*

### 5. Run the application
```bash
python app.py
```
Open your browser and navigate to **`http://localhost:5000`**.

---

##  Cloud Deployment (Render.com)

1. Fork or push this repository to GitHub.
2. Sign in to [Render](https://render.com/) and click **New +** → **Web Service**.
3. Link your GitHub repository.
4. Configure the service:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. In **Environment Variables**, add:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GOOGLE_API_KEY` (optional)
6. Click **Deploy Web Service**.

---

##  Sample Queries to Try

- `"which is the best club?"` ➔ Displays IEEE BMSCE and club profiles.
- `"canteen timings"` ➔ Covers all 4 campus canteens and timings.
- `"are teachers strict?"` ➔ Activates contradiction engine for balanced multi-faculty insights.
- `"attandance strict"` ➔ Tests typo-tolerance on 85% attendance criteria.
- `"highest package cse"` ➔ Displays BMSCE placement statistics & top recruiters.

---
