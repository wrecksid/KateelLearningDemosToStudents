// Loan Default Predictor - Credit Risk Assessment
// Demonstrates ML-based lending decision

class LoanDefaultPredictor {
  constructor() {
    this.init();
  }

  init() {
    // Bind events
    const inputs = ['loan-amount', 'annual-income', 'credit-score', 'employment'];
    inputs.forEach(id => {
      document.getElementById(id).addEventListener('input', (e) => {
        const value = e.target.value;
        const displayId = id.replace(/-(\w)/g, (m, p) => p.toUpperCase());
        document.getElementById(displayId).textContent = value;
        this.predict();
      });
    });

    // Initial prediction
    this.predict();
  }

  predict() {
    const loanAmount = parseInt(document.getElementById('loan-amount').value);
    const income = parseInt(document.getElementById('annual-income').value);
    const creditScore = parseInt(document.getElementById('credit-score').value);
    const employment = parseInt(document.getElementById('employment').value);

    // Calculate DTI
    const dti = (loanAmount / income) * 36;

    // Risk factors (weighted)
    const creditFactor = Math.max(0, (850 - creditScore) / 500);
    const dtiFactor = Math.min(dti / 50, 1);
    const employmentFactor = Math.max(0, 1 - employment / 10);
    const loanSizeFactor = Math.min(loanAmount / 100000, 1);

    // Combined risk score
    const riskScore = (creditFactor * 0.4 + dtiFactor * 0.3 + employmentFactor * 0.2 + loanSizeFactor * 0.1);
    const probability = Math.min(1, Math.max(0, riskScore));

    // Update UI
    const probPercent = Math.round(probability * 100);
    document.getElementById('probability').textContent = `${probPercent}%`;
    document.getElementById('risk-fill').style.width = `${probability * 100}%`;

    // Recommendation
    const recommendation = document.getElementById('recommendation');
    if (probability < 0.3) {
      recommendation.textContent = 'Recommended: Approve automatically';
      recommendation.style.color = '#10b981';
    } else if (probability < 0.6) {
      recommendation.textContent = 'Recommended: Approve with conditions';
      recommendation.style.color = '#f59e0b';
    } else {
      recommendation.textContent = 'Recommended: Decline or require co-signer';
      recommendation.style.color = '#ef4444';
    }

    // Feature importance
    this.updateFeatureImportance(creditScore, dti, employment, loanAmount);
  }

  updateFeatureImportance(creditScore, dti, employment, loanAmount) {
    const container = document.getElementById('feature-importance');
    const features = [
      { name: 'Credit Score', value: creditScore, impact: 'High' },
      { name: 'Debt-to-Income', value: dti.toFixed(1) + '%', impact: dti > 30 ? 'High' : 'Medium' },
      { name: 'Employment Length', value: employment + ' years', impact: employment < 2 ? 'High' : 'Low' },
      { name: 'Loan Size', value: '$' + (loanAmount / 1000).toFixed(0) + 'K', impact: loanAmount > 50000 ? 'Medium' : 'Low' }
    ];

    container.innerHTML = features.map(f => `
      <div class="feature-item">
        <span class="feature-name">${f.name}: ${f.value}</span>
        <span class="feature-value">${f.impact} Impact</span>
      </div>
    `).join('');
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new LoanDefaultPredictor();
});