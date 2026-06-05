// A/B Testing Framework - Statistical Significance Demo

class ABTestingFramework {
  constructor() {
    this.init();
  }

  init() {
    // Bind value displays
    ['control', 'treatment'].forEach(type => {
      document.getElementById(`${type}-input`).addEventListener('input', (e) => {
        document.getElementById(`${type}-rate`).textContent = e.target.value + '%';
      });
    });
    
    document.getElementById('sample-input').addEventListener('input', (e) => {
      document.getElementById('sample-size').textContent = parseInt(e.target.value).toLocaleString();
    });

    document.getElementById('mde-input').addEventListener('input', (e) => {
      document.getElementById('mde-value').textContent = e.target.value + '%';
    });

    document.getElementById('baseline-input').addEventListener('input', (e) => {
      document.getElementById('baseline-value').textContent = e.target.value + '%';
    });

    // Bind button
    document.getElementById('calculate-btn').addEventListener('click', () => this.calculate());

    // Initial calculation
    this.calculate();
  }

  calculate() {
    const controlRate = parseFloat(document.getElementById('control-input').value) / 100;
    const treatmentRate = parseFloat(document.getElementById('treatment-input').value) / 100;
    const sampleSize = parseInt(document.getElementById('sample-input').value);

    // Calculate p-value (two-proportion z-test approximation)
    const pooled = (controlRate + treatmentRate) / 2;
    const se = Math.sqrt(pooled * (1 - pooled) * (2 / sampleSize));
    const z = (treatmentRate - controlRate) / se;
    const pValue = this.pValue(z);

    // Calculate lift
    const lift = ((treatmentRate - controlRate) / controlRate) * 100;

    // Update UI
    document.getElementById('p-value').textContent = pValue.toFixed(3);
    document.getElementById('lift').textContent = lift.toFixed(0) + '%';
    document.getElementById('significant').textContent = pValue < 0.05 ? 'Yes' : 'No';

    const conclusion = document.getElementById('conclusion');
    if (pValue < 0.05) {
      conclusion.textContent = 'Result: Statistically significant difference detected (p < 0.05)';
      conclusion.style.background = '#d1fae5';
      conclusion.style.color = '#065f46';
    } else {
      conclusion.textContent = 'Result: No statistically significant difference (p >= 0.05)';
      conclusion.style.background = '#fee2e2';
      conclusion.style.color = '#991b1b';
    }

    // Calculate required sample size
    this.calculateSampleSize();
  }

  pValue(z) {
    // Approximate p-value from z-score
    // Using approximation for two-tailed test
    const p = 2 * (1 - this.normalCDF(Math.abs(z)));
    return Math.max(0, Math.min(1, p));
  }

  normalCDF(x) {
    // Standard normal cumulative distribution
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

    return 0.5 * (1.0 + sign * y);
  }

  calculateSampleSize() {
    const mde = parseFloat(document.getElementById('mde-input').value) / 100;
    const baseline = parseFloat(document.getElementById('baseline-input').value) / 100;

    // Simplified sample size calculation
    // n = 16 * p(1-p) / delta^2 (for 80% power, 5% significance)
    const p = baseline;
    const delta = baseline * mde;
    const n = Math.ceil(16 * p * (1 - p) / (delta * delta));

    document.getElementById('required-sample').textContent = n.toLocaleString();
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new ABTestingFramework();
});