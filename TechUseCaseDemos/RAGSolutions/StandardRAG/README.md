# Standard RAG Demo

Browser-based demonstration of Retrieval-Augmented Generation using keyword matching and rule-based response generation.

## Live Demo

Open `index.html` in your browser.

## How It Works

1. **Retrieve**: Find relevant chunks from knowledge base using keyword matching
2. **Augment**: Combine query with retrieved context
3. **Generate**: Rule-based system produces answer from context

## Features

- **Document Upload**: Add your own .txt files to the knowledge base
- **Sample Knowledge Base**: 5 pre-loaded documents on AI/ML topics
- **Keyword-based Retrieval**: Find relevant content by matching terms
- **Rule-based Generation**: Answers generated from retrieved context
- **Interactive Interface**: Simple query and response workflow

## Usage

1. Click "Load Knowledge Base" for sample documents
2. Or click "Upload Document" to add your own text files
3. Type a question and click "Ask"
4. View retrieved chunks and generated answer

## Exercises

1. Load sample docs and ask about "machine learning"
2. Ask about "neural networks"
3. Ask about "transformers"
4. Upload your own document and query it

## File Structure

```
StandardRAG/
├── index.html    # Main interface
├── style.css     # Styling
├── app.js        # RAG logic
└── README.md     # This file
```