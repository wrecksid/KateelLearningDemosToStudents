# BFSI Chatbot: Product FAQ Retrieval Demo

## Overview

This demo shows a lightweight retrieval-based chatbot pattern for BFSI product FAQs. It does not use a hosted LLM. Instead, it demonstrates the core retrieval step: matching a user query to the most relevant knowledge-base section.

This is a good teaching bridge between FAQ systems, search, retrieval-augmented generation, and production support assistants.

## Files in This Folder

- `knowledge_base.md` source knowledge snippets
- `faq_chatbot_demo.py` retrieval demo for matching questions to FAQ sections
- `requirements.txt` local dependencies

## How To Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python faq_chatbot_demo.py
```

## Suggested Extensions

- add more product and policy sections
- build a small Streamlit UI
- return multiple ranked passages instead of one
- add evaluation questions and score retrieval quality
