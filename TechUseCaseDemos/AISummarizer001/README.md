# AI Summarizer Demo - Transcript to Bullet Points

A browser-based text summarization tool that converts long transcripts or articles into concise bullet-point summaries using extractive summarization.

## Features

- 📝 **Text Input**: Paste any transcript or article
- 🔍 **Extractive Summarization**: Uses word frequency algorithm
- • **Bullet Point Output**: Clean, scannable key points
- 💾 **Save Summaries**: History stored in localStorage
- 📋 **Copy to Clipboard**: One-click copy functionality

## How to Run

1. Open `index.html` in any modern browser
2. Paste your text/transcript into the textarea
3. Click "Summarize to Bullet Points"
4. Review the key points generated
5. Save or copy the summary as needed

## Demo Points for Students

### 1. Text Processing Pipeline
```
Input Text → Sentence Splitting → Word Frequency → Sentence Scoring → Ranking → Output
```

### 2. Extractive Summarization Algorithm
- Counts word frequency (ignoring stopwords)
- Scores sentences based on important word occurrences
- Returns top N sentences as bullets

### 3. Browser Storage
```javascript
// Save to localStorage
localStorage.setItem('summarizedNotes', JSON.stringify(history));

// Retrieve from localStorage
const history = JSON.parse(localStorage.getItem('summarizedNotes') || '[]');
```

## Key Code Concepts

```javascript
// Word frequency analysis
const wordFreq = {};
words.forEach(word => {
  if (!stopwords.has(word)) {
    wordFreq[word] = (wordFreq[word] || 0) + 1;
  }
});

// Score sentences
sentences.forEach(sentence => {
  const score = sentenceWords.reduce((sum, word) => sum + (wordFreq[word] || 0), 0);
});
```

## Extending This Demo

### Option 1: LLM Integration
Replace the `extractKeyPoints` method with an actual LLM call:

```javascript
async extractKeyPoints(text) {
  const response = await fetch('/api/summarize', {
    method: 'POST',
    body: JSON.stringify({ text })
  });
  return response.json();
}
```

### Option 2: Different Algorithms
- **Leadership TextRank**: Graph-based sentence ranking
- **BERT Extractive**: Use sentence transformers
- **TF-IDF**: Term frequency-inverse document frequency

## Learning Outcomes

- Text preprocessing and NLP basics
- Algorithm implementation (word frequency)
- Working with browser storage
- Building responsive UI for AI features
- Understanding extractive vs abstractive summarization

## Browser Compatibility

All modern browsers (Chrome, Firefox, Safari, Edge)