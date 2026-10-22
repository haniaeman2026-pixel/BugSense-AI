# BugSense AI — AI-Powered Bug Report Analyzer

BugSense AI transforms a natural-language software bug description into a structured report using the **Groq API** and a **LangGraph** workflow.

## Features

- Bug title, affected feature, and issue summary
- Severity classification: Critical, High, Medium, or Low
- Plausible root-cause hypotheses
- Formatted bug report with an investigation note
- Professional responsive UI with example prompts and copy-report action
- FastAPI backend and health endpoint
- API key loaded from `.env` (never commit the key)

## LangGraph workflow

`START → Bug Analysis → Severity Detection → Root Cause Suggestion → Format Report → END`

The four required processing nodes are separate functions in `app/graph.py`. The report is AI-generated; severity and root causes must be verified against actual impact, logs, reproduction steps, and code.

## Requirements

- Windows 10/11
- Python 3.11 or 3.12 recommended
- Internet connection
- Groq API key

Get an API key from the Groq Console: https://console.groq.com/keys

## Run on Windows PowerShell

Open PowerShell in the `BugSense-AI` folder.

### 1. Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.12 is not installed, use `py -m venv .venv`.

If PowerShell blocks activation, run this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure Groq

```powershell
Copy-Item .env.example .env
notepad .env
```

Replace `replace_with_your_groq_api_key` with your own key, save, and close Notepad. Keep `.env` private and do not upload it to GitHub.

### 4. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** in your browser. Keep the terminal open while using the app.

API docs: http://127.0.0.1:8000/docs  
Health check: http://127.0.0.1:8000/api/health

Stop the server with `Ctrl+C`.

## Troubleshooting

- **Missing API key:** confirm `.env` is in the root `BugSense-AI` folder and contains `GROQ_API_KEY=...`.
- **Authentication error:** check the key in the Groq Console and ensure your account/model access is available.
- **Quota/rate limit:** wait and retry, or review your Groq rate limits and usage.
- **Port already in use:** run `python -m uvicorn app.main:app --reload --port 8001` and open `http://127.0.0.1:8001`.
- **Dependency/install issue:** use Python 3.11 or 3.12 in a fresh `.venv`, then reinstall `requirements.txt`.

## Project structure

```text
BugSense-AI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── prompts.py
│   ├── state.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Responsible use

BugSense AI does not inspect the application's source code, runtime, logs, or production environment. Root-cause suggestions are hypotheses based on the description, not confirmed diagnoses. Review all generated output before using it in a real incident or release process.
