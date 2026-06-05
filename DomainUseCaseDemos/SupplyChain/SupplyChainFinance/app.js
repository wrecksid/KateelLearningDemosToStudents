// Supply Chain Finance - Trade Credit Optimization

class SupplyChainFinance {
  constructor() {
    this.init();
  }

  init() {
    ['revenue', 'dso', 'suppliers', 'payment-terms'].forEach(id => {
      document.getElementById(id).addEventListener('input', (e) => {
        document.getElementById(`${id}-val`).textContent = e.target.value + (id === 'revenue' ? 'M' : id === 'dso' || id === 'payment-terms' ? ' days' : ' suppliers');
        this.calculate();
      });
    });
    this.calculate();
  }

  calculate() {
    const revenue = parseInt(document.getElementById('revenue').value) * 1000000;
    const dso = parseInt(document.getElementById('dso').value);
    const suppliers = parseInt(document.getElementById('suppliers').value);
    const paymentTerms = parseInt(document.getElementById('payment-terms').value);
    
    // Cash flow release
    const dailyRevenue = revenue / 365;
    const cashFlowRelease = dailyRevenue * (paymentTerms - dso);
    
    // Discount rate (simplified)
    const discountRate = 0.025;
    const annualSavings = cashFlowRelease * discountRate;
    
    // ROI
    const roi = (annualSavings / revenue) * 100;
    
    document.getElementById('cash-flow').textContent = '$' + (cashFlowRelease / 1000).toFixed(0) + 'K';
    document.getElementById('discount').textContent = (discountRate * 100) + '%';
    document.getElementById('savings').textContent = '$' + (annualSavings / 1000).toFixed(0) + 'K';
    document.getElementById('roi').textContent = roi.toFixed(1) + '%';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new SupplyChainFinance();
});