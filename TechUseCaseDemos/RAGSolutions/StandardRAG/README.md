# Standard RAG Demo

Browser-based demonstration of Retrieval-Augmented Generation using keyword matching and rule-based response generation.

## Live Demo

Open `index.html` in your browser.

## How It Works

1. **Retrieve**: Find relevant chunks from knowledge base using keyword matching
2. **Augment**: Combine query with retrieved context
3. **Generate**: Rule-based system produces answer from context

## Features

- Simulated knowledge base with 5 documents
- Keyword-based retrieval
- Rule-based answer generation
- Interactive query interface

## Exercises

1. Ask about "machine learning"
2. Ask about "neural networks"
3. Ask about "transformers"
4. Ask about "nlp"

## File Structure

```
StandardRAG/
├── index.html    # Main interface
├── style.css     # Styling
├── app.js        # RAG logic
└── README.md     # This file
```