# Graph RAG Demo

Browser-based demonstration of Knowledge Graph-based Retrieval-Augmented Generation.

## Live Demo

Open `index.html` in your browser.

## How Graph RAG Works

1. **Build Graph**: Entities as nodes, relationships as edges
2. **Traverse**: Find relevant paths between query and data
3. **Reason**: Use graph structure for inference
4. **Generate**: LLM answers from graph context

## Knowledge Graph Structure

```
[AI] → subset → [ML]
[AI] → uses → [Neural Networks]
[AI] → applies_to → [NLP]
[ML] → enhances → [RAG]
[NLP] → uses → [Transformers]
[RAG] → uses → [Embeddings]
[RAG] → stores_in → [Vector DB]
```

## Exercises

1. Query "neural" - see connected nodes
2. Query "rag" - find related concepts
3. Query "transformer" - explore NLP connections

## Advantages Over Standard RAG

- **Structured reasoning**: Follows explicit relationships
- **Better explainability**: Clear path from query to answer
- **Fewer hallucinations**: Constrained by graph structure
- **Scalable**: Can handle large knowledge bases efficiently

## Note on Document Upload

This demo uses a predefined knowledge graph. For document upload capabilities, see [Standard RAG](../StandardRAG/).

## File Structure

```
GraphRAG/
├── index.html    # Main interface
├── style.css     # Styling
├── app.js        # Graph traversal logic
└── README.md     # This file
```