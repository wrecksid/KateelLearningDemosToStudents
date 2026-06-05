# RAG Solutions - Demo Collection

Browser-based demonstrations of different RAG (Retrieval-Augmented Generation) architectures with voice integration.

## Available Demos

| Demo | Type | Document Upload | Voice I/O | Key Feature |
|------|------|-----------------|-----------|-------------|
| [Standard RAG](StandardRAG/) | Text-based | ✅ | ❌ | Keyword retrieval |
| [Graph RAG](GraphRAG/) | Graph-based | ❌ | ❌ | Knowledge traversal |
| [PageIndex RAG](PageIndexRAG/) | Index-based | ✅ | ❌ | Precise citations |
| [Voice Standard RAG](VoiceStandardRAG/) | Voice + Text RAG | ✅ | ✅ | Voice pipeline |
| [Voice Graph RAG](VoiceGraphRAG/) | Voice + Graph | ❌ | ✅ | Voice + reasoning |
| [Voice PageIndex RAG](VoicePageIndexRAG/) | Voice + Index | ✅ | ✅ | Voice + citations |

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

### Voice RAG Variants
All three RAG types have voice-enabled versions with:
- **STT**: Speech-to-Text for voice input
- **TTS**: Text-to-Speech for spoken output
- **Full pipeline**: Voice → RAG → Voice

## Quick Start

```bash
# Text-based RAG
open TechUseCaseDemos/RAGSolutions/StandardRAG/index.html

# Voice RAG
open TechUseCaseDemos/RAGSolutions/VoiceStandardRAG/index.html
```

## Learning Objectives

- Understand different RAG architectures
- Compare retrieval strategies
- Explore trade-offs in RAG design
- Practice prompt engineering for RAG
- Learn citation and source attribution
- Experience voice-enabled AI interfaces

## Related Courses

- [NLP Course Catalog](../CourseCatalogs/NLP/)
- [Data Mining Course Catalog](../CourseCatalogs/DataMining/)