// Credit Scoring Dashboard - Logistic Regression Demo
// Demonstrates credit scoring model and feature engineering

class CreditScoringDemo {
  constructor() {
    this.weights = {
      income: 0.3,
      debtRatio: -0.4,
      history: 0.25,
      cards: -0.15
    };
    
    this.baseScore = 300;
    this.maxScore = 850;
    
    this.init();
  }

  init() {
    // Bind input events
    document.getElementById('income').addEventListener('input', (e) => this.updateValue('income', e.target.value, 'income-value'));
    document.getElementById('debt').addEventListener('input', (e) => this.updateValue('debt', e.target.value, 'debt-value'));
    document.getElementById('history').addEventListener('input', (e) => this.updateValue('history', e.target.value, 'history-value'));
    document.getElementById('cards').addEventListener('input', (e) => this.updateValue('cards', e.target.value, 'cards-value'));

    // Initial calculation
    this.calculateScore();
  }

  updateValue(id, value, displayId) {
    document.getElementById(displayId).textContent = value.toLocaleString();
    this.calculateScore();
  }

  calculateScore() {
    const income = parseInt(document.getElementById('income').value);
    const debt = parseInt(document.getElementById('debt').value);
    const history = parseInt(document.getElementById('history').value);
    const cards = parseInt(document.getElementById('cards').value);

    // Normalize features
    const incomeScore = Math.min(income / 200000, 1);
    const debtRatio = debt / Math.max(income, 1);
    const debtScore = Math.max(0, 1 - debtRatio * 2);
    const historyScore = Math.min(history / 30, 1);
    const cardsScore = Math.max(0, 1 - cards / 10);

    // Calculate weighted score
    let score = this.baseScore;
    score += incomeScore * 100 * this.weights.income;
    score += debtScore * 100 * this.weights.debtRatio;
    score += historyScore * 100 * this.weights.history;
    score += cardsScore * 100 * this.weights.cards;
    score = Math.min(score, this.maxScore);

    // Update UI
    this.updateScoreDisplay(score);
    this.updateFeatureChart(incomeScore, debtScore, historyScore, cardsScore);
    this.updatePointsBreakdown(incomeScore, debtScore, historyScore, cardsScore);
  }

  updateScoreDisplay(score) {
    const scoreValue = Math.round(score);
    document.getElementById('score-value').textContent = scoreValue;
    document.getElementById('score-display').textContent = scoreValue;
    document.getElementById('score-circle').style.setProperty('--score-percent', `${(scoreValue / this.maxScore) * 360}deg`);

    // Decision logic
    const decisionEl = document.getElementById('decision');
    const riskEl = document.getElementById('risk-level');
    
    if (score >= 650) {
      decisionEl.textContent = 'Approved ✅';
      decisionEl.style.color = '#10b981';
      riskEl.textContent = 'Low Risk';
      riskEl.style.color = '#10b981';
    } else if (score >= 550) {
      decisionEl.textContent = 'Review Required ⚠️';
      decisionEl.style.color = '#f59e0b';
      riskEl.textContent = 'Medium Risk';
      riskEl.style.color = '#f59e0b';
    } else {
      decisionEl.textContent = 'Declined ❌';
      decisionEl.style.color = '#ef4444';
      riskEl.textContent = 'High Risk';
      riskEl.style.color = '#ef4444';
    }
  }

  updateFeatureChart(income, debt, history, cards) {
    const chart = document.getElementById('feature-chart');
    const features = [
      { name: 'Income', value: income, color: '#3b82f6' },
      { name: 'Debt Ratio', value: debt, color: '#10b981' },
      { name: 'History', value: history, color: '#f59e0b' },
      { name: 'Credit Cards', value: cards, color: '#ef4444' }
    ];

    chart.innerHTML = features.map(f => `
      <div class="feature-item">
        <span class="feature-name">${f.name}</span>
        <div class="feature-bar-container">
          <div class="feature-bar" style="width: ${f.value * 100}%; background: ${f.color};"></div>
        </div>
        <span class="feature-value">${Math.round(f.value * 100)}%</span>
      </div>
    `).join('');
  }

  updatePointsBreakdown(income, debt, history, cards) {
    const breakdown = document.getElementById('points-breakdown');
    const items = [
      { label: 'Income Score', value: Math.round(income * 100), positive: income > 0.5 },
      { label: 'Debt Ratio', value: Math.round(debt * 50 - 25), positive: debt > 0.5 },
      { label: 'Credit History', value: Math.round(history * 50), positive: history > 0.5 },
      { label: 'Card Count', value: Math.round(cards * 25 - 25), positive: cards < 3 }
    ];

    breakdown.innerHTML = items.map(item => `
      <div class="points-item">
        <span class="points-label">${item.label}</span>
        <span class="points-value ${item.positive ? 'positive' : 'negative'}">${item.positive ? '+' : ''}${item.value} pts</span>
      </div>
    `).join('');
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new CreditScoringDemo();
});