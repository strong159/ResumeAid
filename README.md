# ResumeAid

ResumeAid is an interactive web application built at hackathons to streamline job preparation. It lets users upload resumes, parse job descriptions, and practice interviews with a built‑in interviewer. Authentication and session handling ensure a smooth, secure experience.

## ✨ Features
- **Resume Upload & Parsing** — extract key skills and experience for matching.
- **Job Description Analysis** — compare resumes against JDs to highlight gaps.
- **Mock Interview** — real‑time Q&A and scoring/feedback.
- **Auth & Sessions** — secure login/registration.
- **Clean UI** — responsive, simple flows for fast testing.

## 🧱 Tech Stack
**Flask, FastAPI, Streamlit**

## 📁 Project Structure (truncated)
```
├── ResumeAid
│   ├── .DS_Store
│   ├── .git
│   │   ├── COMMIT_EDITMSG
│   │   ├── FETCH_HEAD
│   │   ├── HEAD
│   │   ├── branches
│   │   ├── config
│   │   ├── description
│   │   ├── hooks
│   │   ├── index
│   │   ├── info
│   │   ├── logs
│   │   ├── objects
│   │   └── refs
│   ├── .gitattributes
│   ├── .gitignore
│   ├── app.py
│   ├── audio.py
│   ├── bot_for_interview
│   │   ├── .DS_Store
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── build
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── public
│   │   └── src
│   ├── database.json
│   ├── frontend.py
│   ├── frontend_2.py
│   ├── generate_questions.py
│   ├── index.html
│   ├── interview_bot
│   │   ├── .DS_Store
│   │   ├── .git
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── public
│   │   └── src
│   ├── interview_bot_app.py
│   ├── main.py
│   ├── new_index.html
│   ├── package.json
│   ├── questions.json
│   ├── save.py
│   ├── stats.json
│   ├── temp.py
│   ├── temp3.py
│   ├── temp_2.py
│   ├── temp_4.py
│   ├── temp_5.py
│   ├── templates
│   └── test.py
└── __MACOSX
    ├── ._ResumeAid
    └── ResumeAid
        ├── ._.DS_Store
        ├── ._.git
        ├── ._.gitattributes
        ├── ._.gitignore
        ├── ._app.py
        ├── ._audio.py
        ├── ._bot_for_interview
        ├── ._database.json
        ├── ._frontend.py
        ├── ._frontend_2.py
        ├── ._generate_questions.py
        ├── ._index.html
        ├── ._interview_bot
        ├── ._interview_bot_app.py
        ├── ._main.py
        ├── ._new_index.html
        ├── ._package.json
        ├── ._questions.json
        ├── ._save.py
        ├── ._stats.json
        ├── ._temp.py
        ├── ._temp3.py
        ├── ._temp_2.py
        ├── ._temp_4.py
        ├── ._temp_5.py
        ├── ._templates
        ├── ._test.py
        ├── .git
        ├── bot_for_interview
        └── interview_bot
```

## 🔧 Setup

### 1) Clone
```bash
git clone https://github.com/strong159/ResumeAid.git
cd ResumeAid
```

### 2) Create virtual env & install deps
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Create a `requirements.txt` with:
```text
Flask\nfastapi\nflask-cors\nrequests\nstreamlit
```
Then install:
```bash
pip install -r requirements.txt
```

### 3) Environment variables
Create a `.env` (or set environment variables) for any API keys or secrets used by the app, e.g.:
```
SECRET_KEY=change-me
RESUME_API_KEY=your_key_here
```

## ▶️ Run
```bash
export FLASK_APP=ResumeAid/frontend.py
export FLASK_ENV=development  # optional
flask run
```

## ✅ Notes
- Pin versions in `requirements.txt` once verified for reproducibility.
- Do not commit real secrets; commit a `.env.example` instead.

## 📝 License
MIT (or your preferred license)
