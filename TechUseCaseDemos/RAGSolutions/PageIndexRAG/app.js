// PageIndex RAG Demo - Document indexing with page-level retrieval
// Simulates inverted index for precise citation

class PageIndexRAG {
    constructor() {
        this.index = {}; // Inverted index: keyword -> [pages]
        this.documents = [];
        this.sampleDocs = [
            { 
                id: 1, 
                title: "Introduction to Machine Learning", 
                pages: [
                    { num: 1, content: "Machine learning is a field of computer science that uses statistical techniques to enable computers learn from data." },
                    { num: 2, content: "Supervised learning requires labeled training data to make predictions." },
                    { num: 3, content: "Unsupervised learning finds patterns in data without labels." }
                ]
            },
            { 
                id: 2, 
                title: "Deep Learning Fundamentals", 
                pages: [
                    { num: 1, content: "Neural networks are computing systems inspired by biological neural networks." },
                    { num: 2, content: "Deep learning uses multiple layers of neural networks for complex pattern recognition." },
                    { num: 3, content: "Backpropagation is the key algorithm for training neural networks." }
                ]
            },
            { 
                id: 3, 
                title: "Natural Language Processing", 
                pages: [
                    { num: 1, content: "NLP enables computers to understand, interpret and generate human language." },
                    { num: 2, content: "Transformers are the dominant architecture for NLP tasks." },
                    { num: 3, content: "Named entity recognition identifies entities like persons and organizations." }
                ]
            }
        ];
        
        this.init();
    }

    init() {
        document.getElementById('index-btn').addEventListener('click', () => this.indexDocuments());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
        document.getElementById('search-btn').addEventListener('click', () => this.search());
        document.getElementById('query-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.search();
        });
    }

    indexDocuments() {
        this.index = {};
        this.documents = [];
        
        this.sampleDocs.forEach(doc => {
            this.documents.push(doc);
            doc.pages.forEach(page => {
                const words = page.content.toLowerCase().split(/\s+/);
                words.forEach(word => {
                    if (!this.index[word]) this.index[word] = [];
                    this.index[word].push({ docId: doc.id, pageNum: page.num, title: doc.title });
                });
            });
        });
        
        this.renderDocuments();
        this.updateStatus(`Indexed ${this.documents.length} documents`);
    }

    renderDocuments() {
        const el = document.getElementById('documents');
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

    updateStatus(msg) {
        const el = document.getElementById('documents');
        if (this.documents.length === 0) {
            el.innerHTML = `<p class="hint">${msg}</p>`;
        }
    }

    search() {
        const query = document.getElementById('query-input').value.trim().toLowerCase();
        if (!query || Object.keys(this.index).length === 0) return;

        const terms = query.split(/\s+/);
        const results = {};
        
        terms.forEach(term => {
            if (this.index[term]) {
                this.index[term].forEach(page => {
                    const key = `${page.docId}-${page.pageNum}`;
                    if (!results[key]) {
                        results[key] = { ...page, content: '' };
                    }
                });
            }
        });
        
        this.renderResults(results, query);
        this.generateAnswer(query, results);
    }

    renderResults(results, query) {
        const el = document.getElementById('results');
        const entries = Object.entries(results);
        
        if (entries.length === 0) {
            el.innerHTML = '<p class="hint">No results found.</p>';
            return;
        }
        
        let html = '';
        entries.forEach(([key, page]) => {
            html += `<div class="result-item"><span class="citation">p.${page.pageNum}</span> ${page.title}</div>`;
        });
        
        el.innerHTML = html;
    }

    generateAnswer(query, results) {
        const answerEl = document.getElementById('answer');
        const entries = Object.entries(results);
        
        if (entries.length === 0) {
            answerEl.innerHTML = '<p>No information found to answer your query.</p>';
            return;
        }
        
        let answer = `<p><strong>Answer for "${query}":</strong></p><ul>`;
        
        entries.forEach(([key, page]) => {
            answer += `<li><span class="citation-link">p.${page.pageNum}</span> ${page.title}: `;
            answer += `Relevant information about ${query} can be found on page ${page.pageNum}.</li>`;
        });
        
        answer += '</ul>';
        answer += `<p><em>Using PageIndex RAG enables precise source attribution for factual accuracy and audit trails.</em></p>`;
        
        answerEl.innerHTML = answer;
    }

    clear() {
        this.index = {};
        this.documents = [];
        document.getElementById('documents').innerHTML = '<p class="hint">Click "Index Documents" to load sample documents.</p>';
        document.getElementById('results').innerHTML = '<p class="hint">Search results will appear here...</p>';
        document.getElementById('answer').innerHTML = '<p>Search for information and generate answers with page citations...</p>';
        document.getElementById('query-input').value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PageIndexRAG();
});