# PageIndex RAG Demo

Browser-based demonstration of document indexing with page-level retrieval for precise citations.

## Live Demo

Open `index.html` in your browser.

## How PageIndex RAG Works

1. **Index**: Create inverted index mapping keywords to page references
2. **Retrieve**: Find pages matching query keywords
3. **Cite**: Return page numbers with results
4. **Generate**: LLM answers with precise citations

## Key Features

- **Precise Citations**: Every answer includes page numbers
- **Source Attribution**: Exact document and page references
- **Audit Trail**: Clear traceability for factual claims
- **Efficiency**: Fast keyword lookup via inverted index

## Advantages

| Feature | PageIndex RAG | Standard RAG |
|---------|---------------|--------------|
| Source Attribution | ✅ Page-level | ❌ Chunk-level |
| Audit Trail | ✅ Exact pages | ❌ Approximate |
| Hallucination Risk | Lower | Higher |
| Citation Accuracy | High | Moderate |

## Exercises

1. Click "Index Documents"
2. Search for "machine learning"
3. Search for "neural"
4. Observe page citations in answers

## File Structure

```
PageIndexRAG/
├── index.html    # Main interface
├── style.css     # Styling
├── app.js        # Indexing logic
└── README.md     # This file
```