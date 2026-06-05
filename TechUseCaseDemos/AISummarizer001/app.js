// AI Summarizer Demo - Transcript to Bullet Points
// Uses extractive summarization (word frequency) - no external API needed
// Students can extend this with actual LLM integration

class AISummarizer {
  constructor() {
    this.summarizeBtn = document.getElementById('summarize-btn');
    this.transcriptInput = document.getElementById('transcript-input');
    this.resultsSection = document.getElementById('results-section');
    this.summaryList = document.getElementById('summary-list');
    this.historySection = document.getElementById('history-section');
    this.historyList = document.getElementById('history-list');
    this.copyBtn = document.getElementById('copy-btn');
    this.saveBtn = document.getElementById('save-btn');
    this.copyToast = document.getElementById('copy-toast');

    this.bindEvents();
    this.loadHistory();
  }

  bindEvents() {
    this.summarizeBtn.addEventListener('click', () => this.summarize());
    this.copyBtn.addEventListener('click', () => this.copySummary());
    this.saveBtn.addEventListener('click', () => this.saveSummary());
  }

  summarize() {
    const text = this.transcriptInput.value.trim();
    if (!text) {
      alert('Please enter some text to summarize.');
      return;
    }

    // Show loading state
    this.summarizeBtn.disabled = true;
    this.summarizeBtn.textContent = 'Summarizing...';

    // Simulate processing delay for demo
    setTimeout(() => {
      const bullets = this.extractKeyPoints(text);
      this.displaySummary(bullets);
      
      this.summarizeBtn.disabled = false;
      this.summarizeBtn.textContent = 'Summarize to Bullet Points';
    }, 500);
  }

  // Extractive summarization using word frequency
  extractKeyPoints(text, maxPoints = 8) {
    // Split into sentences
    const sentences = text
      .replace(/([.!?])\s*(?=[A-Z])/g, '$1|SENTENCE_BREAK|')
      .split('|SENTENCE_BREAK|')
      .filter(s => s.trim().length > 10);

    // Remove extra whitespace
    const cleanSentences = sentences.map(s => s.trim().replace(/\s+/g, ' '));

    // Word frequency (stopwords removed)
    const stopwords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
      'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'this',
      'that', 'these', 'those', 'it', 'its', 'as', 'if', 'then', 'than',
      'so', 'such', 'no', 'not', 'only', 'own', 'same', 'too', 'very',
      'just', 'also', 'now', 'here', 'there', 'when', 'where', 'why', 'how'
    ]);

    // Count word frequency
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const wordFreq = {};
    words.forEach(word => {
      if (!stopwords.has(word) && word.length > 2) {
        wordFreq[word] = (wordFreq[word] || 0) + 1;
      }
    });

    // Score sentences
    const sentencesWithScores = cleanSentences.map(sentence => {
      const sentenceWords = sentence.toLowerCase().match(/\b\w+\b/g) || [];
      let score = 0;
      sentenceWords.forEach(word => {
        score += wordFreq[word] || 0;
      });
      return { sentence, score };
    });

    // Sort by score and return top sentences
    const topSentences = sentencesWithScores
      .sort((a, b) => b.score - a.score)
      .slice(0, maxPoints)
      .map(item => item.sentence);

    return topSentences;
  }

  displaySummary(bullets) {
    this.resultsSection.classList.remove('hidden');
    this.historySection.classList.remove('hidden');

    // Render bullet points
    this.summaryList.innerHTML = bullets.map(bullet => `<li>${bullet}</li>`).join('');
    
    // Scroll to results
    this.resultsSection.scrollIntoView({ behavior: 'smooth' });
  }

  copySummary() {
    const text = this.summaryList.innerText;
    navigator.clipboard.writeText(text).then(() => {
      this.copyToast.classList.remove('hidden');
      setTimeout(() => {
        this.copyToast.classList.add('hidden');
      }, 2000);
    });
  }

  saveSummary() {
    const summaryText = this.summaryList.innerText;
    const originalText = this.transcriptInput.value.trim();
    
    const history = JSON.parse(localStorage.getItem('summarizedNotes') || '[]');
    const newEntry = {
      id: Date.now().toString(),
      original: originalText,
      summary: summaryText,
      timestamp: new Date().toISOString()
    };
    history.unshift(newEntry);
    localStorage.setItem('summarizedNotes', JSON.stringify(history));
    
    this.loadHistory();
    alert('Summary saved!');
  }

  loadHistory() {
    const history = JSON.parse(localStorage.getItem('summarizedNotes') || '[]');
    if (history.length === 0) {
      this.historySection.classList.add('hidden');
      return;
    }

    this.historyList.innerHTML = history.map(item => `
      <div class="history-item" onclick="app.loadSummary('${item.id}')">
        <div>${item.original.substring(0, 80)}${item.original.length > 80 ? '...' : ''}</div>
        <div class="history-time">${new Date(item.timestamp).toLocaleString()}</div>
      </div>
    `).join('');
    
    this.historySection.classList.remove('hidden');
  }

  loadSummary(id) {
    const history = JSON.parse(localStorage.getItem('summarizedNotes') || '[]');
    const item = history.find(h => h.id === id);
    if (item) {
      this.transcriptInput.value = item.original;
      this.displaySummary(item.summary.split('\n').filter(Boolean));
    }
  }
}

// Global app instance
let app;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  app = new AISummarizer();
});