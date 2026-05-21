# 📋 PROJECT SPECIFICATION: Client-Side In-Browser SLM Demos

## 1. Overview & Objective

The goal is to build a suite of isolated, zero-dependency, pure client-side web application demos demonstrating the use of Small Language Models (SLMs) running **100% locally in the browser** via hardware acceleration (WebGPU/WASM). These are added to the student-facing repository `KateelLearningDemosToStudents` to demonstrate edge AI capabilities without cloud API dependencies.

---

## 2. Tech Stack & Architectural Rules

| Layer | Choice |
|---|---|
| **Frontend** | Vanilla HTML5, CSS3 (modern responsive styling), native JavaScript (ES6+ Modules) |
| **Dependencies** | None to install — AI frameworks imported via CDN (`https://cdn.jsdelivr.net/npm/`) |
| **AI Engine 1** | Transformers.js v3 for lightweight task-specific SLM workloads |
| **AI Engine 2** | WebLLM for streaming conversational instruction-tuned SLMs |
| **Environment** | Windows 11 Native Win32 · Chromium-based browsers (Chrome/Edge) with WebGPU enabled |

---

## 3. Sub-Project Specifications

### 📂 Demo 1: The Privacy-First Local Chat Advisor
- **Directory:** `Browser-AI-Product-Demos/1-local-chat-advisor/`
- **Core Task:** A standard, beautiful chat interface (like ChatGPT) that lets students talk to an AI advisor completely offline.
- **Model Config:** `onnx-community/SmolLM2-135M-Instruct` via Transformers.js v3 pipeline
- **UI/UX Requirements:**
  - Clean, responsive layout with a top status bar indicating download status in `%`
  - Explicit status toggle: `⚪ Downloading Components` ➡️ `🟢 Offline AI Engine Ready`
  - System prompt hardcoded: *"You are an expert academic study buddy. Keep your answers concise, structured, and use encouraging language."*

### 📂 Demo 2: The E-Commerce Smart Ticket Tagger
- **Directory:** `Browser-AI-Product-Demos/2-customer-support-tagger/`
- **Core Task:** Real-time customer sentiment and request routing categorization as the customer types their support ticket.
- **Model Config:** `Xenova/distilbert-base-uncased-finetuned-sst-2-english` (sentiment) + `Xenova/nli-deberta-v3-small` (zero-shot classification) via Transformers.js
- **UI/UX Requirements:**
  - **Left Column:** Form text-area for typing an email or complaint
  - **Right Column:** Real-time analysis gauges — debounce 300ms then update:
    - Sentiment: (`🔴 Frustrated/Angry`, `🟡 Neutral`, `🟢 Satisfied`)
    - Urgency: (`High` / `Medium` / `Low`)
    - Auto-Route Department: (`Billing`, `Tech Support`, `Product Feedback`)

### 📂 Demo 3: Local AI Note-Taking Copilot
- **Directory:** `Browser-AI-Product-Demos/3-privacy-notebook/`
- **Core Task:** A rich text editing notepad where users can use shortcut buttons to rewrite, fix grammar, or summarize sensitive data safely — all offline.
- **Model Config:** `Xenova/t5-small` via Transformers.js text2text-generation pipeline
- **UI/UX Requirements:**
  - A text area resembling a clean document pad
  - A floating tool-dock with buttons: `✨ Professional Polish`, `📝 Condense to TL;DR`, `🔍 Fix Grammar`
  - An output preview block showing the new text stream without page refreshes

---

## 4. Coding Standards

- **No Node/NPM overhead** — pure static files, no `package.json`, `webpack`, or `vite` configs
- **State management** — local only; model weights cache automatically via the browser's Cache Storage
- **Error resilience** — gracefully catch WebGPU unavailability and fall back to CPU WASM with an on-screen notice

---

## 5. Development Workflow

```powershell
# Run a local verification server from the Browser-AI-Product-Demos directory
npx serve .
```

Then open Chrome or Edge to `http://localhost:3000`.

> **WebGPU check:** `chrome://gpu` → look for **WebGPU: Enabled**

---

## 6. Implemented Demos

| # | Demo | Model | Size |
|---|---|---|---|
| 1 | [Local Chat Advisor](Browser-AI-Product-Demos/1-local-chat-advisor/index.html) | SmolLM2-135M-Instruct | ~135 MB |
| 2 | [Smart Ticket Tagger](Browser-AI-Product-Demos/2-customer-support-tagger/index.html) | DistilBERT SST-2 + DeBERTa NLI | ~140 MB |
| 3 | [Privacy Notebook](Browser-AI-Product-Demos/3-privacy-notebook/index.html) | T5-Small | ~60 MB |
