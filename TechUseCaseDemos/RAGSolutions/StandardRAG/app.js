// Standard RAG Demo - Browser Implementation
// Simulates RAG pipeline using keyword matching and rule-based generation
// Supports document upload for custom knowledge bases

class StandardRAG {
    constructor() {
        this.knowledgeBase = [];
        this.sampleDocs = [
            { id: 1, content: "Machine learning is a subset of artificial intelligence that enables systems to learn from data.", keywords: ["machine", "learning", "ai", "algorithm"], source: "sample" },
            { id: 2, content: "Neural networks are computing systems inspired by biological neural networks.", keywords: ["neural", "network", "brain", "deep"], source: "sample" },
            { id: 3, content: "Natural language processing enables computers to understand human language.", keywords: ["nlp", "language", "text", "speech"], source: "sample" },
            { id: 4, content: "Transformers are neural networks designed for sequence-to-sequence tasks.", keywords: ["transformer", "sequence", "attention", "bert"], source: "sample" },
            { id: 5, content: "Vector databases store embeddings for efficient similarity search.", keywords: ["vector", "database", "embedding", "search"], source: "sample" }
        ];
        
        this.init();
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadKnowledgeBase());
        document.getElementById('upload-btn').addEventListener('click', () => document.getElementById('file-input').click());
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
        document.getElementById('ask-btn').addEventListener('click', () => this.askQuestion());
        document.getElementById('query-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.askQuestion();
        });
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
        const id = this.knowledgeBase.length + 1;
        const words = text.toLowerCase().split(/\s+/);
        const keywords = [...new Set(words.filter(w => w.length > 3))];
        
        this.knowledgeBase.push({
            id: id,
            content: text.substring(0, 5000),
            keywords: keywords,
            source: filename
        });
        
        this.renderKnowledgeBase();
        this.updateStatus(`Added "${filename}" to knowledge base`);
    }

    loadKnowledgeBase() {
        this.knowledgeBase = this.sampleDocs.map(d => ({ ...d }));
        this.renderKnowledgeBase();
        this.updateStatus('Knowledge base loaded with 5 sample documents');
    }

    renderKnowledgeBase() {
        const kbEl = document.getElementById('knowledge-base');
        kbEl.innerHTML = '';
        
        this.knowledgeBase.forEach(doc => {
            const div = document.createElement('div');
            div.className = 'kb-item';
            div.innerHTML = `<strong>[${doc.id}]</strong> ${doc.source || 'sample'}: ${doc.content.substring(0, 80)}...`;
            kbEl.appendChild(div);
        });
        
        this.updateStatus('', true);
    }

    updateStatus(msg, keepContent = false) {
        const kbEl = document.getElementById('knowledge-base');
        if (!keepContent && this.knowledgeBase.length === 0) {
            kbEl.innerHTML = `<p class="hint">${msg || 'Knowledge base is empty. Load sample docs or upload your own.'}</p>`;
        } else if (keepContent) {
            // Already rendered content
        } else {
            kbEl.innerHTML += `<p class="hint" style="margin-top: 10px;">${msg}</p>`;
        }
    }

    askQuestion() {
        const query = document.getElementById('query-input').value.trim();
        if (!query) return;

        const retrieved = this.retrieve(query);
        this.renderRetrieved(retrieved);
        const answer = this.generate(query, retrieved);
        this.renderAnswer(answer);
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

    renderRetrieved(docs) {
        const el = document.getElementById('retrieved');
        if (docs.length === 0) {
            el.innerHTML = '<p class="hint">No relevant documents found.</p>';
            return;
        }
        
        el.innerHTML = docs.map(doc => 
            `<div class="chunk">Chunk ${doc.id} (${doc.source}): ${doc.content.substring(0, 80)}...</div>`
        ).join('');
    }

    generate(query, docs) {
        if (docs.length === 0) {
            return "I don't have enough information to answer that question. Try asking about machine learning, neural networks, or NLP. Or upload your own documents!";
        }
        
        const context = docs.map(d => d.content).join(' ');
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('transformer')) {
            return "Transformers are neural networks designed for sequence-to-sequence tasks like translation and text generation. They use self-attention mechanisms to process input data in parallel, making them much faster than previous recurrent networks. Key models include BERT, GPT, and T5.";
        }
        if (queryLower.includes('neural')) {
            return "Neural networks are computing systems loosely inspired by biological neural networks in the brain. They consist of layers of interconnected nodes (neurons) that process information and learn patterns from data. Deep neural networks have multiple hidden layers and can model complex relationships.";
        }
        if (queryLower.includes('machine learning')) {
            return "Machine learning is a subset of artificial intelligence that enables systems to learn from data rather than explicit programming. It includes supervised learning (predictions), unsupervised learning (clustering), and reinforcement learning (decision-making). Applications include recommendation systems, fraud detection, and autonomous vehicles.";
        }
        if (queryLower.includes('nlp')) {
            return "Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language. Key techniques include tokenization, part-of-speech tagging, named entity recognition, and sentiment analysis. Modern NLP heavily relies on transformer models like BERT and GPT.";
        }
        
        return `Based on your documents: ${context.substring(0, 200)}... This relates to your question about "${query}".`;
    }

    renderAnswer(answer) {
        document.getElementById('answer').innerHTML = `<p>${answer}</p>`;
    }

    clear() {
        this.knowledgeBase = [];
        document.getElementById('knowledge-base').innerHTML = '<p class="hint">Knowledge base is empty. Load sample docs or upload your own.</p>';
        document.getElementById('retrieved').innerHTML = '<p class="hint">Retrieved chunks will appear here...</p>';
        document.getElementById('answer').innerHTML = '<p>Ask a question to see the RAG response...</p>';
        document.getElementById('query-input').value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StandardRAG();
});