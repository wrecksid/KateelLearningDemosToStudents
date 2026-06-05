// Counter Party Risk - CVA Calculation Demo

class CounterPartyRisk {
  constructor() {
    this.creditRatings = {
      AAA: { pd: 0.001, lgd: 0.4 },
      AA: { pd: 0.002, lgd: 0.45 },
      A: { pd: 0.005, lgd: 0.5 },
      BBB: { pd: 0.012, lgd: 0.55 },
      BB: { pd: 0.035, lgd: 0.6 },
      B: { pd: 0.08, lgd: 0.65 },
      CCC: { pd: 0.15, lgd: 0.7 }
    };
    
    this.init();
  }

  init() {
    document.getElementById('credit-rating').addEventListener('change', () => this.calculate());
    ['notional', 'maturity', 'collateral'].forEach(id => {
      document.getElementById(id).addEventListener('input', (e) => {
        document.getElementById(`${id}-val`).textContent = e.target.value;
        this.calculate();
      });
    });
    
    this.calculate();
  }

  calculate() {
    const rating = document.getElementById('credit-rating').value;
    const notional = parseInt(document.getElementById('notional').value) * 100000;
    const maturity = parseInt(document.getElementById('maturity').value);
    const collateral = parseInt(document.getElementById('collateral').value) / 100;

    const { pd, lgd } = this.creditRatings[rating];
    
    // Simplified CVA calculation
    const avgExposure = notional * 0.52;
    const cva = avgExposure * pd * lgd * (1 - collateral);
    
    // Update UI
    document.getElementById('pd').textContent = (pd * 100).toFixed(2) + '%';
    document.getElementById('lgd').textContent = (lgd * 100).toFixed(0) + '%';
    document.getElementById('exposure').textContent = '$' + (avgExposure / 1000000).toFixed(1) + 'M';
    document.getElementById('cva').textContent = '$' + (cva / 1000).toFixed(0) + 'K';
    document.getElementById('mortgage').textContent = '$' + (cva / 1000).toFixed(0) + 'K';
    document.getElementById('collateral-impact').textContent = '-$' + ((cva * collateral) / 1000).toFixed(0) + 'K';
    document.getElementById('net-cva').textContent = '$' + ((cva * (1 - collateral)) / 1000).toFixed(0) + 'K';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new CounterPartyRisk();
});