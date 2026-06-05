// Fraud Detection Playground - Anomaly Detection Demo
// Uses isolation forest-like scoring for fraud detection

class FraudDetectionPlayground {
  constructor() {
    this.transactions = [];
    this.fraudLabels = [];
    
    this.init();
  }

  init() {
    // Bind events
    document.getElementById('run-btn').addEventListener('click', () => this.runDetection());
    document.getElementById('txn-count-input').addEventListener('input', (e) => {
      document.getElementById('txn-count').textContent = e.target.value;
    });
    document.getElementById('fraud-rate-input').addEventListener('input', (e) => {
      document.getElementById('fraud-rate').textContent = e.target.value + '%';
    });
    document.getElementById('threshold-input').addEventListener('input', (e) => {
      document.getElementById('threshold-value').textContent = e.target.value;
    });

    // Initial run
    this.generateTransactions();
    this.runDetection();
  }

  generateTransactions() {
    const count = parseInt(document.getElementById('txn-count-input').value);
    const fraudRate = parseInt(document.getElementById('fraud-rate-input').value) / 100;
    
    this.transactions = [];
    this.fraudLabels = [];

    for (let i = 0; i < count; i++) {
      // Normal transaction features
      const amount = Math.random() * 5000 + 10;
      const merchant = Math.floor(Math.random() * 5);
      const hour = Math.floor(Math.random() * 24);
      
      this.transactions.push({
        amount,
        merchant,
        hour,
        x: Math.random() * 100,
        y: Math.random() * 100
      });

      // Mark some as fraud
      if (Math.random() < fraudRate) {
        this.fraudLabels.push(1);
        // Fraudulent transactions have unusual patterns
        this.transactions[this.transactions.length - 1].amount *= 3;
        this.transactions[this.transactions.length - 1].merchant = Math.floor(Math.random() * 10) + 5;
        this.transactions[this.transactions.length - 1].x += 50;
        this.transactions[this.transactions.length - 1].y += 50;
      } else {
        this.fraudLabels.push(0);
      }
    }
  }

  runDetection() {
    const threshold = parseFloat(document.getElementById('threshold-input').value);
    
    // Simple anomaly score based on distance from center
    const scores = this.transactions.map(t => {
      const distance = Math.sqrt(Math.pow(t.x - 50, 2) + Math.pow(t.y - 50, 2));
      const anomalyScore = distance / 100;
      return anomalyScore;
    });

    // Predictions
    const predictions = scores.map(score => score > threshold ? 1 : 0);

    // Calculate metrics
    const tp = predictions.filter((p, i) => p === 1 && this.fraudLabels[i] === 1).length;
    const fp = predictions.filter((p, i) => p === 1 && this.fraudLabels[i] === 0).length;
    const fn = predictions.filter((p, i) => p === 0 && this.fraudLabels[i] === 1).length;

    const precision = tp / (tp + fp) || 0;
    const recall = tp / (tp + fn) || 0;
    const f1 = 2 * (precision * recall) / (precision + recall) || 0;

    // Update UI
    document.getElementById('precision').textContent = `${Math.round(precision * 100)}%`;
    document.getElementById('recall').textContent = `${Math.round(recall * 100)}%`;
    document.getElementById('f1-score').textContent = `${Math.round(f1 * 100)}%`;
    document.getElementById('fraud-found').textContent = tp;

    // Draw chart
    this.drawScatterChart(scores, predictions);
  }

  drawScatterChart(scores, predictions) {
    const canvas = document.getElementById('scatter-chart');
    const ctx = canvas.getContext('2d');
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const margin = 50;
    const chartW = canvas.width - margin * 2;
    const chartH = canvas.height - margin * 2;

    // Draw grid
    ctx.strokeStyle = '#e2e8f0';
    for (let i = 0; i <= 5; i++) {
      const x = margin + (i / 5) * chartW;
      ctx.beginPath();
      ctx.moveTo(x, margin);
      ctx.lineTo(x, canvas.height - margin);
      ctx.stroke();
      
      const y = margin + (i / 5) * chartH;
      ctx.beginPath();
      ctx.moveTo(margin, y);
      ctx.lineTo(canvas.width - margin, y);
      ctx.stroke();
    }

    // Draw transactions
    this.transactions.forEach((t, i) => {
      const x = margin + (t.x / 100) * chartW;
      const y = canvas.height - margin - (t.y / 100) * chartH;
      
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      
      if (predictions[i] === 1) {
        ctx.fillStyle = '#ef4444';
      } else {
        ctx.fillStyle = '#10b981';
      }
      ctx.fill();
    });

    // Legend
    ctx.fillStyle = '#10b981';
    ctx.fillRect(20, 20, 15, 15);
    ctx.fillStyle = '#0f172a';
    ctx.font = '12px sans-serif';
    ctx.fillText('Normal', 40, 32);

    ctx.fillStyle = '#ef4444';
    ctx.fillRect(100, 20, 15, 15);
    ctx.fillStyle = '#0f172a';
    ctx.fillText('Fraud Detected', 120, 32);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new FraudDetectionPlayground();
});