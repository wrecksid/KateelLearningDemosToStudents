# RAG Solutions - Demo Collection

Browser-based demonstrations of different RAG (Retrieval-Augmented Generation) architectures.

## Available Demos

| Demo | Type | Description | Document Upload |
|------|------|-------------|-----------------|
| [Standard RAG](StandardRAG/) | Text-based | Keyword matching retrieval | ✅ Yes |
| [Graph RAG](GraphRAG/) | Graph-based | Knowledge graph traversal | ❌ Predefined |
| [PageIndex RAG](PageIndexRAG/) | Index-based | Document indexing with citations | ✅ Yes |

## What is RAG?

Retrieval-Augmented Generation combines:
1. **Information Retrieval**: Finding relevant context
2. **Language Generation**: Producing answers from context

## Demo Types

### Standard RAG
- Retrieves text chunks from document store
- Uses keyword matching for retrieval
- Supports custom document upload
- Best for: General QA, document summarization

### Graph RAG
- Stores information as knowledge graph
- Traverses relationships for reasoning
- Predefined knowledge graph
- Best for: Multi-hop reasoning, structured data

### PageIndex RAG
- Indexes content by page/location
- Precise citation with page numbers
- Document upload with citation tracking
- Best for: Fact verification, academic papers

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
- Learn citation and source attribution

## Related Courses

- [NLP Course Catalog](../CourseCatalogs/NLP/)
- [Data Mining Course Catalog](../CourseCatalogs/DataMining/)