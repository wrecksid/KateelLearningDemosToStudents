// Voice Graph RAG Demo
// Voice + Knowledge Graph + Speech Output

class VoiceGraphRAG {
    constructor() {
        this.graph = {
            nodes: [
                { id: 'ml', label: 'Machine Learning' },
                { id: 'ai', label: 'Artificial Intelligence' },
                { id: 'nn', label: 'Neural Networks' },
                { id: 'nlp', label: 'Natural Language Processing' },
                { id: 'transformer', label: 'Transformers' },
                { id: 'rag', label: 'RAG' }
            ],
            edges: [
                { from: 'ai', to: 'ml', label: 'subset' },
                { from: 'ai', to: 'nn', label: 'uses' },
                { from: 'ai', to: 'nlp', label: 'applies_to' },
                { from: 'ml', to: 'rag', label: 'enhances' },
                { from: 'nlp', to: 'transformer', label: 'uses' },
                { from: 'rag', to: 'nn', label: 'uses' }
            ]
        };
        
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
                if (this.isListening) {
                    this.recognition.start();
                }
            };
        }
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadGraph());
        document.getElementById('mic-btn').addEventListener('click', () => this.toggleListening());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
    }

    loadGraph() {
        this.renderGraph();
        this.updateStatus('kb', 'Graph loaded');
    }

    renderGraph() {
        const el = document.getElementById('graph-viz');
        let html = '<div style="margin-bottom: 10px;"><strong>Nodes:</strong></div>';
        
        this.graph.nodes.forEach(node => {
            html += `<span class="node">${node.label}</span>`;
        });
        
        html += '<div style="margin-top: 15px;"><strong>Relationships:</strong></div>';
        
        this.graph.edges.forEach(edge => {
            const fromLabel = this.graph.nodes.find(n => n.id === edge.from)?.label || edge.from;
            const toLabel = this.graph.nodes.find(n => n.id === edge.to)?.label || edge.to;
            html += `<div class="edge">${fromLabel} → ${edge.label} → ${toLabel}</div>`;
        });
        
        el.innerHTML = html;
    }

    updateStatus(type, msg) {
        const el = document.getElementById(`${type}-status`);
        if (el) el.textContent = `${type === 'stt' ? '🎤' : '🔊'} ${type === 'stt' ? 'STT' : 'TTS'}: ${msg}`;
    }

    toggleListening() {
        if (!this.recognition) {
            alert('Speech recognition not supported.');
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
            this.updateDisplay('query', 'Listening... please speak now.');
        }
    }

    handleQuery(query) {
        this.updateDisplay('query', `Question: ${query}`);
        this.updateStatus('stt', 'Processing...');
        
        const path = this.traverse(query);
        const answer = this.generate(query, path);
        
        this.updateDisplay('path', `Path: ${path.join(' → ')}`);
        this.updateDisplay('response', answer);
        this.updateStatus('stt', 'Ready');
        this.speak(answer);
    }

    updateDisplay(type, text) {
        if (type === 'query') document.getElementById('query-display').innerHTML = `<p>${text}</p>`;
        else if (type === 'response') document.getElementById('response-display').innerHTML = `<p>${text}</p>`;
        else if (type === 'path') document.getElementById('path-display').innerHTML = `<p>${text}</p>`;
    }

    traverse(query) {
        const queryLower = query.toLowerCase();
        const path = [];
        
        // Simple keyword matching to find starting node
        for (const node of this.graph.nodes) {
            if (queryLower.includes(node.id) || queryLower.includes(node.label.toLowerCase())) {
                path.push(node.label);
                // Find connected nodes
                this.graph.edges.forEach(edge => {
                    if (edge.from === node.id) {
                        const connected = this.graph.nodes.find(n => n.id === edge.to);
                        if (connected) path.push(connected.label);
                    }
                });
                break;
            }
        }
        
        return path.length > 0 ? path : ['No matching nodes found'];
    }

    generate(query, path) {
        if (path.length === 0) return "I couldn't find relevant information in the knowledge graph.";
        
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('rag')) {
            return "Graph RAG enhances traditional RAG by using a knowledge graph structure. It enables structured reasoning over explicit relationships between entities for more accurate answers.";
        }
        
        return `Based on the knowledge graph, your query relates to: ${path.join(', ')}. Graph RAG uses these relationships for structured reasoning.`;
    }

    speak(text) {
        this.updateStatus('tts', 'Speaking...');
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        
        utterance.onend = () => this.updateStatus('tts', 'Ready');
        this.synthesis.speak(utterance);
    }

    clear() {
        document.getElementById('graph-viz').innerHTML = '<p class="hint">Click "Load Knowledge Graph" to begin.</p>';
        document.getElementById('query-display').innerHTML = '<p class="hint">Your question will appear here after speaking...</p>';
        document.getElementById('path-display').innerHTML = '<p class="hint">Graph path will be shown here...</p>';
        document.getElementById('response-display').innerHTML = '<p class="hint">System response will appear here...</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VoiceGraphRAG();
});