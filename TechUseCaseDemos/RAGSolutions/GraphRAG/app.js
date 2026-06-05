// Graph RAG Demo - Knowledge Graph based retrieval
// Simulates graph traversal and reasoning

class GraphRAG {
    constructor() {
        this.graph = {
            nodes: [
                { id: 'ml', label: 'Machine Learning' },
                { id: 'ai', label: 'Artificial Intelligence' },
                { id: 'nn', label: 'Neural Networks' },
                { id: 'nlp', label: 'Natural Language Processing' },
                { id: 'transformer', label: 'Transformers' },
                { id: 'rag', label: 'RAG' },
                { id: 'embedding', label: 'Embeddings' },
                { id: 'vector', label: 'Vector DB' }
            ],
            edges: [
                { from: 'ai', to: 'ml', label: 'subset' },
                { from: 'ai', to: 'nn', label: 'uses' },
                { from: 'ai', to: 'nlp', label: 'applies_to' },
                { from: 'ml', to: 'nn', label: 'enables' },
                { from: 'nn', to: 'transformer', label: 'evolves_to' },
                { from: 'nlp', to: 'transformer', label: 'uses' },
                { from: 'rag', to: 'embedding', label: 'uses' },
                { from: 'rag', to: 'vector', label: 'stores_in' },
                { from: 'vector', to: 'transformer', label: 'embeds' },
                { from: 'ml', to: 'rag', label: 'enhances' }
            ]
        };
        this.loaded = false;
        
        this.init();
    }

    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadGraph());
        document.getElementById('clear-btn').addEventListener('click', () => this.clear());
        document.getElementById('query-btn').addEventListener('click', () => this.query());
        document.getElementById('query-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.query();
        });
    }

    loadGraph() {
        this.loaded = true;
        this.renderGraph();
        this.updateStatus('Knowledge graph loaded with 8 nodes and 10 edges');
    }

    renderGraph() {
        const el = document.getElementById('graph-viz');
        let html = '<div style="margin-bottom: 10px;"><strong>Nodes:</strong></div>';
        
        this.graph.nodes.forEach(node => {
            html += `<span class="node">${node.label}</span>`;
        });
        
        html += '<div style="margin-top: 15px;"><strong>Relationships:</strong></div>';
        
        this.graph.edges.forEach(edge => {
            const from = this.graph.nodes.find(n => n.id === edge.from)?.label || edge.from;
            const to = this.graph.nodes.find(n => n.id === edge.to)?.label || edge.to;
            html += `<div class="edge">${from} → ${edge.label} → ${to}</div>`;
        });
        
        el.innerHTML = html;
    }

    updateStatus(msg) {
        const el = document.getElementById('graph-viz');
        if (!this.loaded) {
            el.innerHTML = `<p class="hint">${msg}</p>`;
        }
    }

    query() {
        const query = document.getElementById('query-input').value.trim().toLowerCase();
        if (!query || !this.loaded) return;

        const results = this.traverse(query);
        this.renderPath(results);
        this.generateAnswer(query, results);
    }

    traverse(query) {
        // Simple node matching
        const matchingNodes = this.graph.nodes.filter(n => 
            n.label.toLowerCase().includes(query) || n.id.includes(query)
        );
        
        const paths = [];
        
        matchingNodes.forEach(node => {
            // Find connected nodes
            const connected = this.graph.edges
                .filter(e => e.from === node.id || e.to === node.id)
                .map(e => ({
                    node: e.from === node.id ? e.to : e.from,
                    edge: e.label
                }));
            
            paths.push({
                start: node.label,
                connections: connected
            });
        });
        
        return paths;
    }

    renderPath(paths) {
        const el = document.getElementById('path-result');
        
        if (paths.length === 0) {
            el.innerHTML = '<p class="hint">No matching nodes found. Try: "neural", "nlp", "rag", or "transformer"</p>';
            return;
        }
        
        let html = '';
        paths.forEach(p => {
            html += `<div class="edge"><strong>${p.start}</strong><br>`;
            p.connections.forEach(c => {
                const nodeLabel = this.graph.nodes.find(n => n.id === c.node)?.label || c.node;
                html += `&nbsp;→ ${c.edge}: ${nodeLabel}<br>`;
            });
            html += '</div>';
        });
        
        el.innerHTML = html;
    }

    generateAnswer(query, paths) {
        let answer = '';
        
        if (query.includes('rag')) {
            answer = "Graph RAG enhances traditional RAG by using a knowledge graph structure. Instead of retrieving text chunks, it traverses relationships between entities to find more relevant context. This enables reasoning over structured knowledge and provides more accurate answers with better explainability.";
        } else if (query.includes('transformer')) {
            answer = "Transformers are neural networks using self-attention mechanisms. In Graph RAG, transformers help embed entities and relations into vector space, enabling similarity search across the knowledge graph. They power both the retrieval and generation components of modern RAG systems.";
        } else if (query.includes('neural') || query.includes('ml')) {
            answer = "Machine Learning (ML) is a subset of AI that enables systems to learn from data. Neural Networks are computing systems inspired by biological brains. In the context of RAG, ML models power both the retrieval of relevant information and the generation of answers. Graph RAG uses ML to embed graph structures for efficient traversal.";
        } else {
            answer = `Based on the knowledge graph, your query "${query}" connects to: ${paths.map(p => p.start).join(', ')}. Graph RAG uses these relationships to provide structured, reasoning-based answers.`;
        }
        
        document.getElementById('answer').innerHTML = `<p>${answer}</p>`;
    }

    clear() {
        this.loaded = false;
        document.getElementById('graph-viz').innerHTML = '<p class="hint">Graph visualization will appear here...</p>';
        document.getElementById('path-result').innerHTML = '<p class="hint">Path will be shown here...</p>';
        document.getElementById('answer').innerHTML = '<p>Select nodes and explore relationships to generate answers...</p>';
        document.getElementById('query-input').value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new GraphRAG();
});