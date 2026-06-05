# Voice Graph RAG Demo

Voice-enabled Knowledge Graph RAG with Speech-to-Text and Text-to-Speech.

## Live Demo

Open `index.html` in Chrome or Edge with microphone.

## Features

- **Voice Input**: Ask questions by speaking
- **Graph Traversal**: Navigate knowledge graph relationships
- **Structured Reasoning**: Multi-hop inference over entities
- **Voice Output**: Answers spoken aloud

## Usage

1. Click "Load Knowledge Graph"
2. Click microphone and ask about "neural networks" or "rag"
3. Hear the system's spoken response
4. View the traversal path on screen

## Knowledge Graph

```
[AI] → subset → [ML]
[AI] → uses → [Neural Networks]
[AI] → applies_to → [NLP]
[ML] → enhances → [RAG]
[NLP] → uses → [Transformers]
[RAG] → uses → [Neural Networks]
```

## File Structure

```
VoiceGraphRAG/
├── index.html    # Voice interface
├── style.css     # Styling
├── app.js        # Voice + Graph RAG logic
└── README.md     # This file
```