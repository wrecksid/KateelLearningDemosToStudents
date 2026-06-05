// Portfolio Optimizer - Mean-Variance Optimization Demo
// Demonstrates Markowitz portfolio optimization

class PortfolioOptimizer {
  constructor() {
    // Asset expected returns (annual)
    this.returns = {
      spy: 0.10,  // Stocks
      bnd: 0.04,  // Bonds
      gld: 0.06   // Gold
    };

    // Asset volatilities (annual)
    this.volatilities = {
      spy: 0.15,
      bnd: 0.05,
      gld: 0.18
    };

    // Correlation matrix
    this.correlations = {
      spy_bnd: 0.2,
      spy_gld: -0.1,
      bnd_gld: -0.3
    };

    this.init();
  }

  init() {
    // Bind events
    ['spy', 'bnd', 'gld'].forEach(asset => {
      document.getElementById(`${asset}-weight`).addEventListener('input', (e) => {
        this.updateWeight(asset, e.target.value);
      });
    });

    // Initial calculation
    this.calculatePortfolio();
    this.drawFrontier();
  }

  updateWeight(asset, value) {
    const weight = parseInt(value) / 100;
    document.getElementById(`${asset}-value`).textContent = `${weight * 100}%`;
    
    // Enforce weights sum to 100%
    const spyWeight = parseInt(document.getElementById('spy-weight').value) / 100;
    const bndWeight = parseInt(document.getElementById('bnd-weight').value) / 100;
    const gldWeight = parseInt(document.getElementById('gld-weight').value) / 100;
    
    // Normalize if needed
    const total = spyWeight + bndWeight + gldWeight;
    if (total !== 1) {
      const normalized = {
        spy: spyWeight / total,
        bnd: bndWeight / total,
        gld: gldWeight / total
      };
      document.getElementById('spy-value').textContent = `${Math.round(normalized.spy * 100)}%`;
      document.getElementById('bnd-value').textContent = `${Math.round(normalized.bnd * 100)}%`;
      document.getElementById('gld-value').textContent = `${Math.round(normalized.gld * 100)}%`;
    }

    this.calculatePortfolio();
  }

  calculatePortfolio() {
    const w_spy = parseInt(document.getElementById('spy-weight').value) / 100;
    const w_bnd = parseInt(document.getElementById('bnd-weight').value) / 100;
    const w_gld = parseInt(document.getElementById('gld-weight').value) / 100;

    // Expected return
    const expectedReturn = w_spy * this.returns.spy + w_bnd * this.returns.bnd + w_gld * this.returns.gld;

    // Portfolio variance
    const variance = 
      Math.pow(w_spy * this.volatilities.spy, 2) +
      Math.pow(w_bnd * this.volatilities.bnd, 2) +
      Math.pow(w_gld * this.volatilities.gld, 2) +
      2 * w_spy * w_bnd * this.correlations.spy_bnd * this.volatilities.spy * this.volatilities.bnd +
      2 * w_spy * w_gld * this.correlations.spy_gld * this.volatilities.spy * this.volatilities.gld +
      2 * w_bnd * w_gld * this.correlations.bnd_gld * this.volatilities.bnd * this.volatilities.gld;

    const volatility = Math.sqrt(variance);
    const sharpe = (expectedReturn - 0.02) / volatility; // Risk-free rate = 2%

    // Update UI
    document.getElementById('expected-return').textContent = `${(expectedReturn * 100).toFixed(1)}%`;
    document.getElementById('volatility').textContent = `${(volatility * 100).toFixed(1)}%`;
    document.getElementById('sharpe').textContent = sharpe.toFixed(2);
  }

  drawFrontier() {
    const canvas = document.getElementById('frontier-chart');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set up chart
    const margin = 40;
    const chartWidth = canvas.width - margin * 2;
    const chartHeight = canvas.height - margin * 2;

    // Draw axes
    ctx.beginPath();
    ctx.moveTo(margin, margin);
    ctx.lineTo(margin, canvas.height - margin);
    ctx.lineTo(canvas.width - margin, canvas.height - margin);
    ctx.stroke();

    // Draw efficient frontier points (simplified)
    ctx.fillStyle = 'rgba(5, 150, 105, 0.5)';
    for (let risk = 0.02; risk <= 0.25; risk += 0.01) {
      const returnVal = this.calculateReturnForRisk(risk);
      const x = margin + (risk / 0.25) * chartWidth;
      const y = canvas.height - margin - (returnVal / 0.2) * chartHeight;
      
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // Labels
    ctx.fillStyle = '#064e3b';
    ctx.font = '12px sans-serif';
    ctx.fillText('Risk (Vol)', canvas.width / 2 - 30, canvas.height - 10);
    ctx.save();
    ctx.translate(15, canvas.height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Return', 0, 0);
    ctx.restore();
  }

  calculateReturnForRisk(targetRisk) {
    // Simplified efficient frontier calculation
    // In reality, this would use quadratic optimization
    const minRisk = 0.03;
    const maxRisk = 0.22;
    const normalizedRisk = (targetRisk - minRisk) / (maxRisk - minRisk);
    return 0.02 + normalizedRisk * 0.18;
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new PortfolioOptimizer();
});