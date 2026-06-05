// University Knowledge Assistant - Advanced RAG Demo
// Demonstrates: PDF ingestion, Graph RAG, PageIndex, STT, TTS, Local SLM

class UniversityKnowledgeAssistant {
    constructor() {
        this.documents = [];
        this.knowledgeGraph = { nodes: [], edges: [] };
        this.pageIndex = {}; // Inverted index with page refs
        this.settings = {
            useGraphRAG: true,
            usePageIndex: true,
            useSLM: false, // Simulated for browser
            useVoice: true
        };
        
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
        }
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadSampleData());
        document.getElementById('upload-btn').addEventListener('click', () => document.getElementById('file-input').click());
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('mic-btn').addEventListener('click', () => this.toggleListening());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
    }

    handleFileUpload(e) {
        const files = e.target.files;
        Array.from(files).forEach(file => {
            if (file.type === 'application/pdf') {
                this.processPDF(file);
            } else {
                this.processText(file);
            }
        });
    }

    processPDF(file) {
        this.updateStatus(`Processing ${file.name}...`);
        // In production: use PDF.js or similar
        // For demo: simulate with sample content
        setTimeout(() => {
            const simulatedContent = `This is simulated content from ${file.name}. In production, this would extract actual text from the PDF using PDF.js.`;
            this.addDocument(simulatedContent, file.name, 'pdf');
        }, 1000);
    }

    processText(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.addDocument(e.target.result, file.name, 'text');
        };
        reader.readAsText(file);
    }

    addDocument(content, filename, type) {
        const id = this.documents.length + 1;
        const pages = this.simulatePages(content);
        
        this.documents.push({
            id,
            filename,
            type,
            content,
            pages
        });

        // Build page index
        pages.forEach((page, idx) => {
            const words = page.content.toLowerCase().split(/\s+/);
            words.forEach(word => {
                if (word.length > 3) {
                    if (!this.pageIndex[word]) this.pageIndex[word] = [];
                    this.pageIndex[word].push({ docId: id, pageNum: page.num, title: filename });
                }
            });
        });

        // Build knowledge graph nodes
        this.knowledgeGraph.nodes.push({
            id: `doc_${id}`,
            label: filename,
            type: 'document',
            docId: id
        });

        // Add sample entities
        const entities = this.extractEntities(content);
        entities.forEach(entity => {
            this.knowledgeGraph.nodes.push({
                id: entity.id,
                label: entity.name,
                type: entity.type
            });
            this.knowledgeGraph.edges.push({
                from: `doc_${id}`,
                to: entity.id,
                label: 'mentions'
            });
        });

        this.renderDocuments();
        this.renderGraph();
        this.updateStatus(`Added ${filename}`);
    }

    simulatePages(content) {
        // Split content into simulated pages
        const words = content.split(/\s+/);
        const pages = [];
        for (let i = 0; i < Math.min(3, Math.ceil(words.length / 50)); i++) {
            const start = i * 50;
            const end = Math.min(start + 50, words.length);
            pages.push({
                num: i + 1,
                content: words.slice(start, end).join(' ')
            });
        }
        return pages;
    }

    extractEntities(content) {
        // Simple entity extraction for demo
        const entities = [];
        const topics = ['finance', 'banking', 'loan', 'interest', 'security', 'network'];
        
        topics.forEach((topic, idx) => {
            if (content.toLowerCase().includes(topic)) {
                entities.push({ id: `entity_${idx}`, name: topic, type: 'concept' });
            }
        });
        
        return entities;
    }

    loadSampleData() {
        this.addDocument(
            "University of Technology offers undergraduate and graduate programs in Computer Science, Engineering, and Business. The university has a strong focus on research and innovation. Students can access financial aid and scholarship programs.",
            "university-info.pdf",
            "pdf"
        );
        
        this.addDocument(
            "Banking operations include deposit services, loan processing, and investment advisory. Security protocols protect customer data and financial transactions. Network infrastructure supports online banking services.",
            "banking-overview.txt",
            "text"
        );
        
        this.updateStatus("Sample data loaded");
    }

    renderDocuments() {
        const el = document.getElementById('documents');
        el.innerHTML = '';
        
        this.documents.forEach(doc => {
            const div = document.createElement('div');
            div.className = 'doc-item';
            div.innerHTML = `<strong>${doc.filename}</strong> (${doc.pages.length} pages)`;
            el.appendChild(div);
        });
    }

    renderGraph() {
        const el = document.getElementById('graph-preview');
        let html = '<div style="font-size: 11px;">';
        
        this.knowledgeGraph.nodes.slice(0, 5).forEach(node => {
            html += `<div style="margin: 5px 0;">• ${node.label} (${node.type})</div>`;
        });
        
        html += '</div>';
        el.innerHTML = html;
    }

    updateStatus(msg) {
        document.getElementById('status').textContent = msg;
    }

    toggleListening() {
        if (!this.recognition) return;
        
        const btn = document.getElementById('mic-btn');
        if (this.isListening) {
            this.recognition.stop();
            btn.classList.remove('listening');
        } else {
            this.recognition.start();
            btn.classList.add('listening');
            this.recognition.onresult = (e) => {
                const text = e.results[0][0].transcript;
                document.getElementById('query-input').value = text;
                this.askQuestion();
            };
        }
        this.isListening = !this.isListening;
    }

    askQuestion() {
        const query = document.getElementById('query-input').value;
        if (!query) return;
        
        this.updateStatus("Processing...");
        
        // Hybrid RAG: Graph + PageIndex retrieval
        const graphResults = this.queryGraph(query);
        const pageResults = this.queryPageIndex(query);
        
        const answer = this.generateAnswer(query, graphResults, pageResults);
        const citations = this.formatCitations(pageResults);
        
        document.getElementById('answer').innerHTML = `<p><strong>Answer:</strong> ${answer}</p>`;
        document.getElementById('citations').innerHTML = `<strong>Sources:</strong> ${citations}`;
        
        this.speak(answer);
        this.updateStatus("Ready");
    }

    queryGraph(query) {
        // Simulate graph traversal
        const results = [];
        const queryLower = query.toLowerCase();
        
        this.knowledgeGraph.edges.forEach(edge => {
            const fromNode = this.knowledgeGraph.nodes.find(n => n.id === edge.from);
            const toNode = this.knowledgeGraph.nodes.find(n => n.id === edge.to);
            
            if (fromNode && toNode && queryLower.includes(toNode.label.toLowerCase())) {
                results.push({ node: toNode, relationship: edge.label });
            }
        });
        
        return results;
    }

    queryPageIndex(query) {
        const terms = query.toLowerCase().split(/\s+/);
        const results = {};
        
        terms.forEach(term => {
            if (this.pageIndex[term]) {
                this.pageIndex[term].forEach(ref => {
                    const key = `${ref.docId}-${ref.pageNum}`;
                    if (!results[key]) {
                        results[key] = { ...ref };
                    }
                });
            }
        });
        
        return Object.values(results);
    }

    generateAnswer(query, graphResults, pageResults) {
        if (pageResults.length > 0) {
            return `Based on your documents, ${pageResults[0].title} (page ${pageResults[0].pageNum}) discusses this topic. The system found ${pageResults.length} relevant pages and ${graphResults.length} graph connections.`;
        }
        
        return "I couldn't find specific information in the documents. Try uploading PDFs or asking about the sample data.";
    }

    formatCitations(results) {
        if (results.length === 0) return "No citations found";
        
        const unique = {};
        results.forEach(r => {
            const key = `${r.title}-p${r.pageNum}`;
            if (!unique[key]) unique[key] = r;
        });
        
        return Object.values(unique).map(r => `${r.title} (p.${r.pageNum})`).join(', ');
    }

    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            speechSynthesis.speak(utterance);
        }
    }

    clear() {
        this.documents = [];
        this.knowledgeGraph = { nodes: [], edges: [] };
        this.pageIndex = {};
        document.getElementById('documents').innerHTML = '<p class="hint">No documents loaded.</p>';
        document.getElementById('graph-preview').innerHTML = '<p class="hint">Graph will appear after ingestion.</p>';
        document.getElementById('answer').innerHTML = '<p>Ask a question to see the answer...</p>';
        document.getElementById('citations').innerHTML = '<p class="hint">Citations will appear here...</p>';
        document.getElementById('query-input').value = '';
        this.updateStatus("Cleared");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UniversityKnowledgeAssistant();
});