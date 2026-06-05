# RAG Solutions - Demo Collection

Browser-based demonstrations of different RAG (Retrieval-Augmented Generation) architectures with voice integration.

## Quick Start

```bash
# Text-based RAG
open TechUseCaseDemos/RAGSolutions/StandardRAG/index.html

# Voice RAG
open TechUseCaseDemos/RAGSolutions/VoiceStandardRAG/index.html
```

## What You'll Learn

- **RAG Fundamentals**: How retrieval-augmented generation works
- **Architecture Comparison**: Text, Graph, and Index-based RAG
- **Voice Integration**: Speech-to-Text and Text-to-Speech pipelines
- **Document Processing**: Keyword matching and indexing strategies
- **Knowledge Representation**: Graph structures and inverted indices

## Available Demos

| Demo | Type | Document Upload | Voice I/O | Key Feature |
|------|------|-----------------|-----------|-------------|
| [Standard RAG](StandardRAG/) | Text-based | ✅ | ❌ | Keyword retrieval |
| [Graph RAG](GraphRAG/) | Graph-based | ❌ | ❌ | Knowledge traversal |
| [PageIndex RAG](PageIndexRAG/) | Index-based | ✅ | ❌ | Precise citations |
| [Voice Standard RAG](VoiceStandardRAG/) | Voice + Text RAG | ✅ | ✅ | Voice pipeline |
| [Voice Graph RAG](VoiceGraphRAG/) | Voice + Graph | ❌ | ✅ | Voice + reasoning |
| [Voice PageIndex RAG](VoicePageIndexRAG/) | Voice + Index | ✅ | ✅ | Voice + citations |

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

## How to Use in Real Life

### Document QA System
- Upload company documents to the RAG system
- Ask questions about policies, procedures, contracts
- Get cited answers with source references

### Voice Assistant
- Use Voice RAG for hands-free document queries
- Ideal for accessibility scenarios
- Voice-enabled knowledge base search

### Knowledge Management
- Build knowledge graphs for domains
- Enable multi-hop reasoning over relationships
- Support complex query answering

## How to Extend

### Add New Documents
1. Click "Load Knowledge Base" or "Upload Document"
2. Add your .txt files
3. Ask questions about the content

### Extend Knowledge Graph
1. Modify `graph.nodes` and `graph.edges` in app.js
2. Add new entity types and relationships
3. Implement new traversal algorithms

### Customize Responses
1. Modify the `generate()` function
2. Add domain-specific response templates
3. Integrate with LLM APIs for better generation

## Related Courses
- [NLP Course Catalog](../CourseCatalogs/NLP/)
- [Data Mining Course Catalog](../CourseCatalogs/DataMining/)

## Technical Details
- **Frontend**: Vanilla JavaScript, no dependencies
- **Speech**: Web Speech API (Chrome/Edge)
- **Storage**: localStorage for documents
- **Compatibility**: Modern browsers with ES6 support