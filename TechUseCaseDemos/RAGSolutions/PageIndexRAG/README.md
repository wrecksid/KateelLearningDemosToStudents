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

- **Document Upload**: Add your own .txt files to the knowledge base
- **Precise Retrieval**: Keyword-based document search
- **Rule-based Generation**: Answers from retrieved context
- **Interactive Interface**: Simple query and response workflow

## Usage

1. Click "Index Documents" to load sample documents
2. Or click "Upload Document" to add your own text files
3. Type a question and click "Search"
4. View retrieved pages and generated answers with citations

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