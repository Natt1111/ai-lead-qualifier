# 🤖 AI Lead Qualifier

AI-powered lead qualification system that scores buying intent and drafts personalized follow-up emails in real-time.

**Stack:** Python · FastAPI · Claude Sonnet 4.5 · Airtable

---

## ✨ What it does

1. Lead submits a form
2. Claude analyzes intent, budget, timeline
3. Returns 0–100 score + Hot/Warm/Cold classification
4. Drafts personalized email response
5. Saves to Airtable CRM

End-to-end in under 5 seconds.

---

## 🏗️ Architecture

---

## 🎯 Engineering highlights

- **Structured outputs** via Claude tool use — zero JSON parsing errors
- **Async FastAPI** with proper event loop handling
- **Fail-fast validation** of env vars at startup
- **Explainable scoring** — UI streams Claude's reasoning live

---

## 🚀 Run locally

```bash
git clone https://github.com/Natt1111/ai-lead-qualifier.git
cd ai-lead-qualifier
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn main:app --reload
```

Open `http://localhost:8000`

---

## 🎨 UI features

Dark-themed cinematic experience: streaming reasoning trace, animated score ring, self-typing email draft, derived intent/urgency stats.

---

## 👋 About

**Natthaporn Gulgalkhai** — AI Automation Specialist  
[LinkedIn](https://linkedin.com/in/natthapon-gulgalkhai) · [Portfolio](https://lumoralab.lovable.app) · ngulgalkhai@gmail.com
