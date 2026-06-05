// Voice Standard RAG Demo
// Integrates Web Speech API (STT) with RAG + TTS

class VoiceStandardRAG {
    constructor() {
        this.knowledgeBase = [];
        this.sampleDocs = [
            { id: 1, content: "Machine learning is a subset of artificial intelligence that enables systems to learn from data.", keywords: ["machine", "learning", "ai", "algorithm"] },
            { id: 2, content: "Neural networks are computing systems inspired by biological neural networks.", keywords: ["neural", "network", "brain", "deep"] },
            { id: 3, content: "Natural language processing enables computers to understand human language.", keywords: ["nlp", "language", "text", "speech"] }
        ];
        
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        
        this.initSpeech();
        this.init();
    }

    initSpeech() {
        // Web Speech API for STT
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.handleQuery(transcript);
            };
            
            this.recognition.onerror = () => {
                this.updateStatus('stt', 'Error');
                this.isListening = false;
            };
            
            this.recognition.onend = () => {
                if (this.isListening) {
                    this.recognition.start();
                }
            };
        }
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadKnowledgeBase());
        document.getElementById('mic-btn').addEventListener('click', () => this.toggleListening());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
    }

    loadKnowledgeBase() {
        this.knowledgeBase = [...this.sampleDocs];
        this.renderKnowledgeBase();
        this.updateStatus('kb', 'Loaded 3 documents');
    }

    renderKnowledgeBase() {
        const kbEl = document.getElementById('knowledge-base');
        kbEl.innerHTML = '';
        this.knowledgeBase.forEach(doc => {
            const div = document.createElement('div');
            div.className = 'kb-item';
            div.innerHTML = `<strong>[${doc.id}]</strong> ${doc.content.substring(0, 60)}...`;
            kbEl.appendChild(div);
        });
    }

    updateStatus(type, msg) {
        const el = document.getElementById(`${type}-status`);
        if (el) el.textContent = `${type === 'stt' ? '🎤' : '🔊'} ${type === 'stt' ? 'STT' : 'TTS'}: ${msg}`;
    }

    toggleListening() {
        if (!this.recognition) {
            alert('Speech recognition not supported in this browser.');
            return;
        }
        
        if (this.isListening) {
            this.recognition.stop();
            this.isListening = false;
            document.getElementById('mic-btn').classList.remove('listening');
            this.updateStatus('stt', 'Stopped');
        } else {
            this.recognition.start();
            this.isListening = true;
            document.getElementById('mic-btn').classList.add('listening');
            this.updateStatus('stt', 'Listening...');
            this.updateQueryDisplay('Listening... please speak now.');
        }
    }

    handleQuery(query) {
        this.updateQueryDisplay(`Question: ${query}`);
        this.updateStatus('stt', 'Processing...');
        
        const retrieved = this.retrieve(query);
        const answer = this.generate(query, retrieved);
        
        this.updateResponseDisplay(answer);
        this.updateStatus('stt', 'Ready');
        this.speak(answer);
    }

    updateQueryDisplay(text) {
        document.getElementById('query-display').innerHTML = `<p><strong>Your Question:</strong> ${text}</p>`;
    }

    updateResponseDisplay(text) {
        document.getElementById('response-display').innerHTML = `<p><strong>System Response:</strong> ${text}</p>`;
    }

    retrieve(query) {
        const queryLower = query.toLowerCase();
        const queryWords = queryLower.split(/\s+/);
        
        return this.knowledgeBase
            .map(doc => ({
                ...doc,
                score: queryWords.reduce((sum, word) => 
                    sum + doc.keywords.filter(k => k.includes(word)).length, 0)
            }))
            .filter(doc => doc.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, 2);
    }

    generate(query, docs) {
        if (docs.length === 0) {
            return "I don't have information about that. Try asking about machine learning or neural networks.";
        }
        
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('machine learning')) {
            return "Machine learning is a subset of artificial intelligence that enables systems to learn from data rather than explicit programming.";
        }
        if (queryLower.includes('neural')) {
            return "Neural networks are computing systems inspired by biological neural networks in the brain.";
        }
        if (queryLower.includes('nlp')) {
            return "Natural Language Processing enables computers to understand, interpret, and generate human language.";
        }
        
        return "Based on your documents, I found relevant information. How can I help you with this topic?";
    }

    speak(text) {
        this.updateStatus('tts', 'Speaking...');
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        
        utterance.onend = () => {
            this.updateStatus('tts', 'Ready');
        };
        
        this.synthesis.speak(utterance);
    }

    clear() {
        this.knowledgeBase = [];
        document.getElementById('knowledge-base').innerHTML = '<p class="hint">Click "Load Knowledge Base" to populate.</p>';
        document.getElementById('query-display').innerHTML = '<p class="hint">Your question will appear here after speaking...</p>';
        document.getElementById('response-display').innerHTML = '<p class="hint">System response will appear here...</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VoiceStandardRAG();
});