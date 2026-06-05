# University Knowledge Assistant Demo

A comprehensive demonstration of advanced RAG concepts combining Graph RAG, PageIndex, Local SLMs, and Voice I/O.

## Live Demo

Open `index.html` in Chrome or Edge with microphone permissions.

## Features

- **PDF Ingestion**: Upload university documents or course materials
- **Graph RAG**: Build knowledge graph of entities and relationships
- **PageIndex**: Page-level citations with inverted index
- **Voice I/O**: Ask questions by voice, get spoken answers
- **Local SLM**: Ready for integration with Phi-3.5/Mistral
- **Hybrid Retrieval**: Combines graph traversal + page indexing

## System Architecture

```
User Query (Voice/Text)
        ↓
    STT (Web Speech API)
        ↓
    Hybrid Retriever
    ├── Graph RAG (FalkorDB)
    └── PageIndex (PageIndex)
        ↓
    Local SLM (llama.cpp/Phi-3.5)
        ↓
    Response Generator
        ↓
    TTS (Web Speech API)
```

## What You'll Learn

1. **Document Ingestion**: PDF/text processing and chunking
2. **Knowledge Graph**: Entity extraction and relationship mapping
3. **PageIndex**: Inverted index with page-level references
4. **Graph RAG**: Multi-hop reasoning over knowledge graph
5. **Voice Pipeline**: Complete STT→RAG→TTS workflow
6. **System Design**: Integrating multiple AI components

## Technical Stack

| Component | Technology |
|-----------|------------|
| PDF Processing | PDF.js (simulated in demo) |
| Knowledge Graph | FalkorDB (local) |
| Indexing | PageIndex (PageIndex library) |
| SLM | Phi-3.5/Mistral via llama.cpp |
| STT/TTS | Web Speech API |
| Frontend | Vanilla JS (no dependencies) |

## How to Extend

### Add FalkorDB Integration
```javascript
// Connect to FalkorDB
const db = new FalkorDB({ host: 'localhost', port: 9292 });

// Create graph
await db.insertEdge('doc_1', 'mentions', 'entity_1');
```

### Add PageIndex Integration
```javascript
// Use PageIndex library
const indexer = new PageIndex();
indexer.addDocument(docId, content, pages);
const results = indexer.search(query);
```

### Add Local SLM
```javascript
// Use llama.cpp via WebGPU
import { LLM } from '@llama-cpp/headless';

const llm = new LLM({ model: 'phi-3.5-q4.gguf' });
const response = await llm.prompt(prompt);
```

## Usage

1. Click "Load Knowledge Base" for sample university documents
2. Or click "Upload PDFs" to add your own documents
3. Click microphone and ask questions like:
   - "What programs does the university offer?"
   - "Tell me about banking security"
4. View answers with page citations
5. Hear answers via text-to-speech

## Demo Limitations

This browser demo simulates:
- FalkorDB graph operations
- PageIndex indexing
- Local SLM responses

For production use:
- Run FalkorDB locally: `docker run -d -p 9292:9292 falkordb/falkordb`
- Use PageIndex Node.js library
- Run llama.cpp with WebGPU support

## File Structure

```
UniversityKnowledgeAssistant/
├── index.html    # Main interface
├── style.css     # Styling
├── app.js        # System logic
└── README.md     # This file
```

## Related Demos

- [Graph RAG](../RAGSolutions/GraphRAG/) - Standalone Graph RAG
- [Voice RAG](../RAGSolutions/VoiceStandardRAG/) - Voice-enabled RAG
- [PageIndex RAG](../RAGSolutions/PageIndexRAG/) - Document indexing with citations