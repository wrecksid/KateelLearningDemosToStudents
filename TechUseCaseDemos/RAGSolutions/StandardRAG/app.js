// Standard RAG Demo - Browser Implementation
// Simulates RAG pipeline using keyword matching and rule-based generation

class StandardRAG {
    constructor() {
        this.knowledgeBase = [];
        this.sampleDocs = [
            { id: 1, content: "Machine learning is a subset of artificial intelligence that enables systems to learn from data.", keywords: ["machine", "learning", "ai", "algorithm"] },
            { id: 2, content: "Neural networks are computing systems inspired by biological neural networks.", keywords: ["neural", "network", "brain", "deep"] },
            { id: 3, content: "Natural language processing enables computers to understand human language.", keywords: ["nlp", "language", "text", "speech"] },
            { id: 4, content: "Transformers are neural networks designed for sequence-to-sequence tasks.", keywords: ["transformer", "sequence", "attention", "bert"] },
            { id: 5, content: "Vector databases store embeddings for efficient similarity search.", keywords: ["vector", "database", "embedding", "search"] }
        ];
        
        this.init();
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadKnowledgeBase());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
        document.getElementById('ask-btn').addEventListener('click', () => this.askQuestion());
        document.getElementById('query-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.askQuestion();
        });
    }

    loadKnowledgeBase() {
        this.knowledgeBase = [...this.sampleDocs];
        this.renderKnowledgeBase();
        this.updateStatus('Knowledge base loaded with 5 documents');
    }

    renderKnowledgeBase() {
        const kbEl = document.getElementById('knowledge-base');
        kbEl.innerHTML = '';
        
        this.knowledgeBase.forEach(doc => {
            const div = document.createElement('div');
            div.className = 'kb-item';
            div.innerHTML = `<strong>[${doc.id}]</strong> ${doc.content.substring(0, 100)}...`;
            kbEl.appendChild(div);
        });
    }

    updateStatus(msg) {
        const kbEl = document.getElementById('knowledge-base');
        if (this.knowledgeBase.length === 0) {
            kbEl.innerHTML = `<p class="hint">${msg}</p>`;
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
            `<div class="chunk">Chunk ${doc.id}: ${doc.content.substring(0, 80)}...</div>`
        ).join('');
    }

    generate(query, docs) {
        if (docs.length === 0) {
            return "I don't have enough information to answer that question. Try asking about machine learning, neural networks, or NLP.";
        }
        
        const context = docs.map(d => d.content).join(' ');
        const queryLower = query.toLowerCase();
        
        // Simple rule-based responses
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
        
        return `Based on the context: ${context.substring(0, 200)}... This relates to your question about "${query}".`;
    }

    renderAnswer(answer) {
        document.getElementById('answer').innerHTML = `<p>${answer}</p>`;
    }

    clear() {
        this.knowledgeBase = [];
        document.getElementById('knowledge-base').innerHTML = '<p class="hint">Knowledge base is empty.</p>';
        document.getElementById('retrieved').innerHTML = '<p class="hint">Retrieved chunks will appear here...</p>';
        document.getElementById('answer').innerHTML = '<p>Ask a question to see the RAG response...</p>';
        document.getElementById('query-input').value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StandardRAG();
});