// AI ROI Calculator - Financial Analysis Demo

class AIROICalculator {
  constructor() {
    this.init();
  }

  init() {
    // Bind events
    const inputs = ['dev-cost', 'maint-cost', 'benefits', 'duration'];
    inputs.forEach(id => {
      document.getElementById(id).addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        const displayId = id.replace(/-(\w)/g, (m, p) => p.toUpperCase());
        if (id === 'dev-cost') document.getElementById(displayId).textContent = val + 'K';
        else if (id === 'maint-cost') document.getElementById(displayId).textContent = val + 'K';
        else if (id === 'benefits') document.getElementById(displayId).textContent = val + 'K';
        else document.getElementById(displayId).textContent = val;
        this.calculate();
      });
    });

    this.calculate();
  }

  calculate() {
    const devCost = parseInt(document.getElementById('dev-cost').value) * 1000;
    const maintCost = parseInt(document.getElementById('maint-cost').value) * 1000;
    const benefits = parseInt(document.getElementById('benefits').value) * 1000;
    const duration = parseInt(document.getElementById('duration').value);

    let totalCost = devCost;
    let totalBenefits = 0;
    let cumulative = -devCost;
    let payback = 'N/A';

    const yearData = [];

    for (let year = 1; year <= duration; year++) {
      totalCost += maintCost;
      totalBenefits += benefits;
      cumulative += benefits - maintCost;
      
      yearData.push({
        year,
        cost: year === 1 ? devCost : maintCost,
        benefit: benefits,
        cumulative
      });

      if (payback === 'N/A' && cumulative >= 0) {
        payback = year;
      }
    }

    const netValue = totalBenefits - totalCost;

    // Update UI
    document.getElementById('total-cost').textContent = '$' + (totalCost / 1000).toFixed(0) + 'K';
    document.getElementById('total-benefits').textContent = '$' + (totalBenefits / 1000).toFixed(0) + 'K';
    document.getElementById('net-value').textContent = '$' + (netValue / 1000).toFixed(0) + 'K';
    document.getElementById('payback').textContent = payback;

    // Recommendation
    const recommendation = document.getElementById('recommendation');
    if (netValue > benefits) {
      recommendation.textContent = 'Recommendation: Strong investment - positive NPV';
      recommendation.style.background = '#d1fae5';
      recommendation.style.color = '#065f46';
    } else if (netValue > 0) {
      recommendation.textContent = 'Recommendation: Consider timeline - break-even within project life';
      recommendation.style.background = '#fef3c7';
      recommendation.style.color = '#92400e';
    } else {
      recommendation.textContent = 'Recommendation: Consider project carefully - negative NPV';
      recommendation.style.background = '#fee2e2';
      recommendation.style.color = '#991b1b';
    }

    // Year table
    const tbody = document.querySelector('#year-table tbody');
    tbody.innerHTML = yearData.map(d => `
      <tr>
        <td>${d.year}</td>
        <td class="${d.cost === devCost ? '' : 'negative'}">$ ${(d.cost/1000).toFixed(0)}K</td>
        <td class="positive">$ ${(d.benefit/1000).toFixed(0)}K</td>
        <td class="${d.cumulative >= 0 ? 'positive' : 'negative'}">$${Math.round(d.cumulative/1000)}K</td>
      </tr>
    `).join('');
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new AIROICalculator();
});