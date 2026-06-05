// Voice Notes App - Speech-to-Text with localStorage
// Demo for students: Web Speech API + Local Storage

class VoiceNotesApp {
  constructor() {
    this.recognition = null;
    this.isRecording = false;
    this.currentTranscript = '';
    this.timerInterval = null;
    this.seconds = 0;
    
    this.init();
  }

  init() {
    // Check browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      this.showError('Speech recognition is not supported in this browser. Use Chrome or Edge.');
      return;
    }

    // Initialize speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.setupRecognition();

    // Bind events
    document.getElementById('record-btn').addEventListener('click', () => this.toggleRecording());
    document.getElementById('clear-btn').addEventListener('click', () => this.clearTranscript());

    // Load saved notes
    this.loadNotes();
  }

  setupRecognition() {
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';

    this.recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      this.currentTranscript += finalTranscript;
      this.updateTranscriptDisplay();
    };

    this.recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error);
      this.stopRecording();
      this.showError(`Error: ${event.error}`);
    };

    this.recognition.onend = () => {
      if (this.isRecording) {
        this.recognition.start();
      }
    };
  }

  toggleRecording() {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      this.startRecording();
    }
  }

  startRecording() {
    this.isRecording = true;
    this.currentTranscript = '';
    this.seconds = 0;
    
    this.recognition.start();
    this.updateUIState('recording');
    this.startTimer();
  }

  stopRecording() {
    this.isRecording = false;
    this.recognition.stop();
    this.updateUIState('stopped');
    this.stopTimer();
    
    // Save if there's content
    if (this.currentTranscript.trim()) {
      this.saveNote(this.currentTranscript);
    }
  }

  updateUIState(state) {
    const recordBtn = document.getElementById('record-btn');
    const micIcon = document.getElementById('mic-icon');
    const timer = document.getElementById('timer');
    const statusText = document.getElementById('status-text');

    if (state === 'recording') {
      recordBtn.classList.add('recording');
      micIcon.textContent = '⏹';
      timer.classList.remove('hidden');
      statusText.textContent = 'Listening...';
    } else {
      recordBtn.classList.remove('recording');
      micIcon.textContent = '🎤';
      timer.classList.add('hidden');
      statusText.textContent = 'Click to start recording';
    }
  }

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.seconds++;
      const mins = String(Math.floor(this.seconds / 60)).padStart(2, '0');
      const secs = String(this.seconds % 60).padStart(2, '0');
      document.getElementById('timer').textContent = `${mins}:${secs}`;
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  updateTranscriptDisplay() {
    document.getElementById('transcript-output').textContent = this.currentTranscript || 'Your transcription will appear here...';
  }

  saveNote(transcript) {
    const notes = JSON.parse(localStorage.getItem('voiceNotes') || '[]');
    const newNote = {
      id: Date.now().toString(),
      text: transcript,
      timestamp: new Date().toISOString(),
      duration: this.seconds
    };
    notes.unshift(newNote);
    localStorage.setItem('voiceNotes', JSON.stringify(notes));
    this.loadNotes();
    this.currentTranscript = '';
    this.updateTranscriptDisplay();
  }

  loadNotes() {
    const notes = JSON.parse(localStorage.getItem('voiceNotes') || '[]');
    const notesList = document.getElementById('notes-list');
    
    if (notes.length === 0) {
      notesList.innerHTML = '<p class="empty-state">No saved notes yet. Record and save to see them here.</p>';
      return;
    }

    notesList.innerHTML = notes.map(note => `
      <div class="note-item" data-id="${note.id}" onclick="app.loadNote('${note.id}')">
        <div>${note.text.substring(0, 100)}${note.text.length > 100 ? '...' : ''}</div>
        <div class="note-time">${new Date(note.timestamp).toLocaleString()}</div>
      </div>
    `).join('');
  }

  loadNote(id) {
    const notes = JSON.parse(localStorage.getItem('voiceNotes') || '[]');
    const note = notes.find(n => n.id === id);
    if (note) {
      this.currentTranscript = note.text;
      this.updateTranscriptDisplay();
    }
  }

  clearTranscript() {
    this.currentTranscript = '';
    this.updateTranscriptDisplay();
  }

  showError(message) {
    console.log(message);
    // In a real app, show a toast notification
    alert(message);
  }
}

// Global app instance
let app;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  app = new VoiceNotesApp();
});