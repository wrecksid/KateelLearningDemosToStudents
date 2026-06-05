# Voice PageIndex RAG Demo

Voice-enabled document indexing with precise page-level citations.

## Live Demo

Open `index.html` in Chrome or Edge with microphone.

## Features

- **Voice Input**: Ask questions by speaking
- **Document Upload**: Add your own .txt files
- **Precise Citations**: Page-level source attribution
- **Voice Output**: Answers spoken aloud

## Usage

1. Click "Index Documents" for samples or "Upload Docs" for your files
2. Click microphone and ask a question
3. Hear the cited answer
4. View source citations on screen

## Advantages

| Feature | Standard RAG | Graph RAG | PageIndex RAG |
|---------|--------------|-----------|---------------|
| Document Upload | ✅ | ❌ | ✅ |
| Voice Input | ✅ | ✅ | ✅ |
| Precise Citations | ❌ | ❌ | ✅ |
| Multi-hop Reasoning | ❌ | ✅ | ❌ |

## File Structure

```
VoicePageIndexRAG/
├── index.html    # Voice interface
├── style.css     # Styling
├── app.js        # Voice + indexing logic
└── README.md     # This file
```