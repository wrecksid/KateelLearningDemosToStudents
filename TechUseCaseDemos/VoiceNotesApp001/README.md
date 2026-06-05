# Voice Notes App - Speech to Text Demo

A browser-based voice notes application that converts speech to text using the Web Speech API and saves transcripts to localStorage.

## Features

- 🎤 **Speech-to-Text**: Real-time transcription using browser's Web Speech API
- 💾 **Local Storage**: Notes are saved locally in the browser
- ⏱️ **Recording Timer**: Visual feedback during recording
- 📱 **Responsive Design**: Works on desktop and mobile

## How to Run

1. Open `index.html` in Chrome or Edge (Speech Recognition requires these browsers)
2. Click the microphone button to start recording
3. Speak naturally - your words will appear as text
4. Notes are automatically saved when you stop recording
5. View your saved notes in the "Saved Notes" section

## Demo Points for Students

1. **Web Speech API**: `webkitSpeechRecognition` interface
2. **Async Handling**: Continuous vs interim results
3. **localStorage**: Persisting data in browser
4. **State Management**: Recording vs stopped states
5. **Timer Implementation**: Using `setInterval`

## Key Code Concepts

```javascript
// Initialize speech recognition
const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

// Handle results
recognition.onresult = (event) => {
  // event.results contains transcript data
};
```

## Browser Compatibility

- Chrome 25+
- Edge 79+
- Safari (limited support)

## Learning Outcomes

- Understanding Web Speech API capabilities
- Working with browser storage APIs
- Building interactive UI with real-time feedback
- Handling media capture in browsers