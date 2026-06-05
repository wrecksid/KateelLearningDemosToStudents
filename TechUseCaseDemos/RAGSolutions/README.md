# RAG Solutions - Demo Collection

Browser-based demonstrations of different RAG (Retrieval-Augmented Generation) architectures.

## Available Demos

|| Demo | Type | Description |
||------|------|-------------|
|| [Standard RAG](StandardRAG/) | Text-based | Keyword matching retrieval |
|| [Graph RAG](GraphRAG/) | Graph-based | Knowledge graph traversal |
|| [PageIndex RAG](PageIndexRAG/) | Index-based | Document indexing with precise citations |

## What is RAG?

Retrieval-Augmented Generation combines:
1. **Information Retrieval**: Finding relevant context
2. **Language Generation**: Producing answers from context

## Demo Types

### Standard RAG
- Retrieves text chunks from document store
- Uses similarity/search for retrieval
- Simple and effective for many use cases

### Graph RAG
- Stores information as knowledge graph
- Traverses relationships for reasoning
- Better for complex, multi-hop queries

### PageIndex RAG
- Indexes content by page/location
- Good for document QA with citations
- Enables precise source attribution

## Quick Start

```bash
# Open any demo in browser
open TechUseCaseDemos/RAGSolutions/StandardRAG/index.html
```

## Learning Objectives

- Understand different RAG architectures
- Compare retrieval strategies
- Explore trade-offs in RAG design
- Practice prompt engineering for RAG

## Related Courses

- [NLP Course Catalog](../CourseCatalogs/NLP/)
- [Data Mining Course Catalog](../CourseCatalogs/DataMining/)