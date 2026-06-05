// Voice PageIndex RAG Demo
// Voice + Document Indexing + Precise Citations + Speech

class VoicePageIndexRAG {
    constructor() {
        this.index = {};
        this.documents = [];
        this.sampleDocs = [
            { id: 1, title: "Introduction to ML", pages: [{ num: 1, content: "Machine learning enables computers to learn from data without explicit programming." }, { num: 2, content: "Supervised learning uses labeled training data." }] },
            { id: 2, title: "Deep Learning", pages: [{ num: 1, content: "Neural networks are computing systems inspired by biological brains." }, { num: 2, content: "Deep learning uses multiple layers for complex pattern recognition." }] }
        ];
        
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        
        this.initSpeech();
        this.init();
    }

    initSpeech() {
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
                if (this.isListening) this.recognition.start();
            };
        }
    }

    init() {
        document.getElementById('index-btn').addEventListener('click', () => this.indexDocuments());
        document.getElementById('upload-btn').addEventListener('click', () => document.getElementById('file-input').click());
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('mic-btn').addEventListener('click', () => this.toggleListening());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
    }

    indexDocuments() {
        this.index = {};
        this.documents = [];
        
        this.sampleDocs.forEach(doc => {
            this.documents.push(doc);
            doc.pages.forEach(page => {
                const words = page.content.toLowerCase().split(/\s+/);
                words.forEach(word => {
                    if (word.length > 3 && !this.index[word]) this.index[word] = [];
                    if (word.length > 3) {
                        this.index[word].push({ docId: doc.id, pageNum: page.num, title: doc.title });
                    }
                });
            });
        });
        
        this.renderDocuments();
        this.updateStatus('stt', 'Indexed 2 documents');
    }

    handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (event) => {
            const text = event.target.result;
            this.addDocument(text, file.name);
            document.getElementById('file-input').value = '';
        };
        reader.readAsText(file);
    }

    addDocument(text, filename) {
        const id = this.documents.length + 1;
        const pages = [{ num: 1, content: text.substring(0, 1000) }];
        
        this.documents.push({ id, title: filename, pages });
        
        pages.forEach(page => {
            const words = page.content.toLowerCase().split(/\s+/);
            words.forEach(word => {
                if (word.length > 3 && !this.index[word]) this.index[word] = [];
                if (word.length > 3) {
                    this.index[word].push({ docId: id, pageNum: page.num, title: filename });
                }
            });
        });
        
        this.renderDocuments();
    }

    renderDocuments() {
        const el = document.getElementById('docs-content');
        el.innerHTML = '';
        this.documents.forEach(doc => {
            const div = document.createElement('div');
            div.className = 'doc-item';
            div.innerHTML = `<div class="doc-title">${doc.title}</div>`;
            doc.pages.forEach(p => {
                div.innerHTML += `<span class="page-ref">p.${p.num}</span>`;
            });
            el.appendChild(div);
        });
    }

    updateStatus(type, msg) {
        const el = document.getElementById(`${type}-status`);
        if (el) el.textContent = `${type === 'stt' ? '🎤' : '🔊'} ${type === 'stt' ? 'STT' : 'TTS'}: ${msg}`;
    }

    toggleListening() {
        if (!this.recognition) return;
        
        this.isListening = !this.isListening;
        const btn = document.getElementById('mic-btn');
        
        if (this.isListening) {
            this.recognition.start();
            btn.classList.add('listening');
            this.updateStatus('stt', 'Listening...');
        } else {
            this.recognition.stop();
            btn.classList.remove('listening');
            this.updateStatus('stt', 'Stopped');
        }
    }

    handleQuery(query) {
        this.updateStatus('stt', 'Processing...');
        const results = this.search(query);
        const answer = this.generate(query, results);
        
        this.renderResults(results);
        this.updateAnswer(answer);
        this.updateStatus('stt', 'Ready');
        this.speak(answer);
    }

    search(query) {
        const terms = query.toLowerCase().split(/\s+/);
        const results = {};
        
        terms.forEach(term => {
            if (this.index[term]) {
                this.index[term].forEach(page => {
                    const key = `${page.docId}-${page.pageNum}`;
                    if (!results[key]) {
                        results[key] = { ...page };
                    }
                });
            }
        });
        
        return results;
    }

    renderResults(results) {
        const el = document.getElementById('results-content');
        const entries = Object.entries(results);
        
        if (entries.length === 0) {
            el.innerHTML = '<p class="hint">No results found.</p>';
            return;
        }
        
        el.innerHTML = entries.map(([key, page]) => 
            `<div class="result-item"><span class="citation">p.${page.pageNum}</span> ${page.title}</div>`
        ).join('');
    }

    updateAnswer(text) {
        document.getElementById('answer').innerHTML = `<p><strong>Answer:</strong> ${text}</p>`;
    }

    generate(query, results) {
        const entries = Object.entries(results);
        if (entries.length === 0) {
            return "No information found. Please upload documents and try again.";
        }
        
        const citations = entries.map(([key, page]) => `page ${page.pageNum} of ${page.title}`).join(', ');
        return `Based on your documents, ${citations}. This information relates to your question about "${query}".`;
    }

    speak(text) {
        this.updateStatus('tts', 'Speaking...');
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.onend = () => this.updateStatus('tts', 'Ready');
        this.synthesis.speak(utterance);
    }

    clear() {
        this.index = {};
        this.documents = [];
        document.getElementById('docs-content').innerHTML = '<p class="hint">Click "Index Documents" to load samples.</p>';
        document.getElementById('results-content').innerHTML = '<p class="hint">Search results will appear here...</p>';
        document.getElementById('answer').innerHTML = '<p>Ask a question by voice to get cited answers...</p>';
        document.getElementById('query-input').value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VoicePageIndexRAG();
});