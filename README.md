# 🐛 AgentiBugger — Agentic Bug Hunter

> Advanced 3-agent orchestration for mission-critical code analysis, powered by Google DeepMind & OpenRouter.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-agenticbugger.vercel.app-blue?style=for-the-badge)](https://agenticbugger.vercel.app/)
[![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/)

---

## 📖 What is AgentiBugger?

AgentiBugger is an **agentic AI pipeline** that autonomously hunts for bugs in code samples. Unlike a simple script, it uses a multi-agent orchestration system that:

- Independently calls an **MCP (Model Context Protocol) Search Tool** to gather relevant documentation context
- Uses a **Gemini 2.0 Flash** model (via OpenRouter) to analyse code with deep semantic understanding
- Combines the code's **Hint**, **Purpose**, and **Documentation** to mimic how a human expert would reason about bugs
- Gracefully **self-heals** when external tools (like the MCP server) are unavailable

The project has both a **web frontend** (Next.js + Vercel) and a **Python backend** (FastAPI) that runs the agentic pipeline.

---

## ✨ Key Features

- **Agentic, not scripted** — The orchestrator autonomously decides how to gather context, adapting when tools fail
- **Self-correcting JSON parser** — Handles common LLM formatting quirks (markdown code fences, missing keys) automatically
- **Context-aware analysis** — Analyses code alongside its hint, purpose, and API documentation for expert-level bug detection
- **MCP resilience** — On MCP server failure, prints a single helpful tip and silently falls back; no error floods
- **Clean CSV output** — Whitespace-normalised output (newlines/tabs collapsed) renders perfectly in Excel
- **Data integrity** — All samples processed in memory and written in a single batch, guaranteeing correct ID sequence with no duplicates
- **Modern web UI** — Drag-and-drop `samples.csv` upload with a sleek Next.js frontend

---

## 🏗️ Architecture

```
samples.csv (Input)
       │
       ▼
  main.py (OrchestratorAgent)
       │
       ├──► MCP Server (Doc Search) ──► Vector DB / API Docs
       │
       ├──► OpenRouter (Gemini 2.0 Flash)
       │
       └──► clean_text() Utility
                  │
                  ▼
          output.csv (Final Result)
```

The web app exposes the same pipeline through a FastAPI backend, with the Next.js frontend handling file upload and result display.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React, Tailwind CSS, Framer Motion |
| Backend / API | FastAPI, Uvicorn, Python |
| AI Model | Gemini 2.0 Flash via OpenRouter |
| Agent Protocol | MCP (Model Context Protocol) |
| Deployment | Vercel |

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Clone the repository

```bash
git clone https://github.com/ashish03124/AgentiBugger.git
cd AgentiBugger
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Start the MCP documentation server (optional but recommended)

```bash
python code/server/mcp_server.py
```

> **Note:** If the MCP server isn't running, the agent will gracefully fall back to analysing code without documentation context. You'll see a single tip in the terminal on how to start it.

### 6. Run the backend

```bash
uvicorn api.main:app --reload
```

### 7. Run the frontend

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📂 Project Structure

```
AgentiBugger/
├── api/                    # FastAPI backend
├── src/
│   └── app/                # Next.js frontend (App Router)
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── next.config.mjs         # Next.js configuration
├── vercel.json             # Vercel deployment config
└── PRESENTATION_NOTES.md   # Technical deep-dive & design decisions
```

---

## 💡 How to Use

1. Navigate to the live app at [agenticbugger.vercel.app](https://agenticbugger.vercel.app/) or run it locally
2. Prepare a `samples.csv` file with your code samples (columns: `id`, `code`, `hint`, `purpose`)
3. Drag and drop or upload the CSV via the web UI
4. The agentic pipeline analyses each sample and produces an `output.csv` with identified bugs and explanations

---

## 🤔 What Makes It "Agentic"?

A plain script runs fixed steps. AgentiBugger's orchestrator:

1. **Uses tools autonomously** — It calls the MCP search tool to pull relevant docs; if the tool is offline, it adapts its strategy instead of crashing
2. **Self-corrects** — The JSON parser handles malformed LLM output automatically
3. **Reasons with context** — It combines code, hints, purpose, and documentation the way a human expert would, not just running a single prompt

---

## 📄 License

This project is private. All rights reserved.

---

<p align="center">Built by <a href="https://github.com/ashish03124">ashish03124</a> • Powered by Google DeepMind & OpenRouter</p>
