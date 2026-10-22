 <div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0B1220,50:172438,100:0B1220&height=220&section=header&text=BugSense%20AI&fontSize=58&fontColor=F2C078&animation=fadeIn&fontAlignY=40&desc=Intelligent%20Bug%20Analysis%20%7C%20Powered%20by%20Groq%20%2B%20LangGraph&descSize=16&descColor=D8E1EE&descAlignY=63" width="100%" alt="BugSense AI Header" />

### AI-Powered Bug Report Analyzer

**Turn bug descriptions into structured insights, severity assessments, and actionable debugging suggestions.**

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-1C3C3C?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-LLM-F0C078?style=for-the-badge)](https://groq.com/)

</div>

---

## 📌 Overview

**BugSense AI** is an AI-powered developer tool designed to simplify bug analysis. It takes a natural-language bug description and uses an AI workflow to generate a structured report with relevant details for debugging and investigation.

The project combines **Groq's language models** with **LangGraph** to organize the analysis into a multi-stage workflow.

## ✨ Key Features

- 🐛 **Bug Analysis** — Extracts a clear bug title, summary, and affected feature.
- 🚦 **Severity Detection** — Estimates the severity as Critical, High, Medium, or Low.
- 🔍 **Root Cause Suggestions** — Provides plausible causes to investigate.
- 📋 **Structured Reports** — Organizes the findings into a readable report.
- ⚡ **LangGraph Workflow** — Separates the analysis into four logical stages.
- 🎨 **Professional UI** — Dark interface with refined gold accents and responsive layouts.
- 📄 **Copy Report** — Copy analysis results for reference or issue tracking.

## ⚙️ How It Works

<div align="center">

| Stage | Process | Output |
|:---:|---|---|
| 01 | Bug Analysis | Title, summary, affected feature |
| 02 | Severity Detection | Estimated severity level |
| 03 | Root Cause Suggestion | Potential causes to investigate |
| 04 | Report Formatting | Structured bug report |

</div>

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | Backend API |
| Groq API | Language-model inference |
| LangGraph | Multi-stage analysis workflow |
| HTML5 | User interface structure |
| CSS3 | Responsive styling |
| JavaScript | Frontend interactions |

## 📂 Project Structure

```text
BugSense-AI/
│
├── app/
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above is a reference. Adjust it to match your actual repository files.*

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/BugSense-AI.git
cd BugSense-AI
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
```

Replace the placeholders with your own valid Groq credentials and a model currently available to your account.

**Security:** Never commit your `.env` file or expose your API key in a public repository.

### 5. Run the Application

```bash
py -m uvicorn app.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

*These commands assume your FastAPI entry point is `app/main.py` and your app is exposed as `app`. Adjust them if your implementation differs.*

## 🔐 Security Notes

- Keep API credentials in environment variables.
- Add `.env` and `.venv/` to `.gitignore`.
- Validate user input before processing it.
- Review AI-generated root-cause suggestions before making code changes.

## 🔮 Future Enhancements

- Integration with GitHub Issues.
- Export reports to Markdown or PDF.
- Bug history and report management.
- Automated test suggestions.
- More detailed debugging recommendations.

## 👩‍💻 Developed By

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0B1220,50:26364B,100:0B1220&height=100&section=footer&text=Hania%20Eman&fontSize=34&fontColor=F2C078&animation=fadeIn&fontAlignY=50" width="100%" alt="Developed by Hania Eman" />

**AI & Data Science Student | Python Developer | AI Project Developer**

*Building practical AI applications through intelligent workflows and thoughtful design.*

</div>

---

<div align="center">

**BugSense AI** · Intelligent Analysis for Better Debugging

<sub>Built with Python, Groq, and LangGraph.</sub>

</div>
