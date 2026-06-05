# Voice Standard RAG Demo

Browser-based Voice + RAG demo with Speech-to-Text (STT) and Text-to-Speech (TTS).

## Live Demo

Open `index.html` in Chrome or Edge with microphone permissions.

## Features

- **Speech-to-Text**: Ask questions by voice
- **Text-to-Speech**: Answers spoken aloud
- **Document Upload**: Add your own .txt files
- **Real-time Processing**: Voice → Answer → Voice pipeline

## Requirements

- Chrome 113+ or Edge 113+
- Microphone permission
- Web Speech API support

## Usage

1. Click "Load Knowledge Base" for sample docs
2. Click the microphone button and speak your question
3. Listen to the system's spoken response
4. View the question and answer on screen

## How It Works

```
🎤 Your Voice → STT → Text Question
                           ↓
📚 Retrieve from Knowledge Base
                           ↓
🤖 Generate Answer
                           ↓
🔊 TTS → Spoken Response
```

## File Structure

```
VoiceStandardRAG/
├── index.html    # Voice interface
├── style.css     # Styling
├── app.js        # STT/TTS/RAG logic
└── README.md     # This file
```