// Black-Scholes Option Pricing Model
// Demonstrates European option pricing and Greeks

class BlackScholesPricer {
  constructor() {
    this.init();
  }

  init() {
    // Bind events
    const params = ['spot', 'strike', 'time', 'vol', 'rate'];
    params.forEach(p => {
      document.getElementById(p).addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        const display = document.getElementById(`${p === 'time' ? 'time' : p === 'rate' ? 'rate' : p}-val`);
        if (p === 'time') display.textContent = (val / 365 * 12).toFixed(1);
        else if (p === 'rate') display.textContent = val.toFixed(2);
        else display.textContent = val.toLocaleString();
        this.calculate();
      });
    });

    this.calculate();
  }

  normCDF(x) {
    const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
    const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);
    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return 0.5 * (1.0 + sign * y);
  }

  calculate() {
    const S = parseFloat(document.getElementById('spot').value);
    const K = parseFloat(document.getElementById('strike').value);
    const T = parseFloat(document.getElementById('time').value) / 365;
    const sigma = parseFloat(document.getElementById('vol').value) / 100;
    const r = parseFloat(document.getElementById('rate').value) / 100;

    // Black-Scholes formula
    const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
    const d2 = d1 - sigma * Math.sqrt(T);

    const call = S * this.normCDF(d1) - K * Math.exp(-r * T) * this.normCDF(d2);
    const put = K * Math.exp(-r * T) * this.normCDF(-d2) - S * this.normCDF(-d1);

    // Greeks
    const Nprime = (x) => Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
    const deltaCall = this.normCDF(d1);
    const deltaPut = deltaCall - 1;
    const gamma = Nprime(d1) / (S * sigma * Math.sqrt(T));
    const theta = -(S * Nprime(d1) * sigma) / (2 * Math.sqrt(T)) - r * K * Math.exp(-r * T) * this.normCDF(d2);
    const vega = S * Math.sqrt(T) * Nprime(d1);
    const rhoCall = K * T * Math.exp(-r * T) * this.normCDF(d2);

    // Update UI
    document.getElementById('call-price').textContent = `$${call.toFixed(2)}`;
    document.getElementById('put-price').textContent = `$${put.toFixed(2)}`;
    document.getElementById('call-delta').textContent = deltaCall.toFixed(2);
    document.getElementById('put-delta').textContent = deltaPut.toFixed(2);
    document.getElementById('gamma').textContent = gamma.toFixed(4);
    document.getElementById('theta').textContent = (theta / 365).toFixed(4);
    document.getElementById('vega').textContent = (vega / 100).toFixed(4);
    document.getElementById('rho-call').textContent = (rhoCall / 100).toFixed(2);

    // Draw chart
    this.drawSurface(S, K, r, sigma, T);
  }

  drawSurface(S, K, r, sigma, T) {
    const canvas = document.getElementById('surface-chart');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw simple heatmap
    const step = 10;
    for (let i = 0; i < 50; i += step) {
      for (let j = 0; j < 50; j += step) {
        const spot = S * (0.5 + i / 100);
        const vol = (10 + j / 50 * 50);
        const d1 = (Math.log(spot / K) + (r + 0.5 * vol * vol / 10000) * T) / (vol / 100 * Math.sqrt(T));
        const price = Math.max(0, spot * this.normCDF(d1) - K * Math.exp(-r * T) * this.normCDF(d1 - vol / 100 * Math.sqrt(T)));
        
        const color = price > 10 ? '#10b981' : price > 5 ? '#f59e0b' : '#ef4444';
        ctx.fillStyle = color;
        ctx.fillRect(i * 8, j * 6, 8, 6);
      }
    }

    // Legend
    ctx.fillStyle = '#065f46';
    ctx.font = '10px sans-serif';
    ctx.fillText('High Value', 10, 15);
    ctx.fillStyle = '#92400e';
    ctx.fillText('Medium', 60, 15);
    ctx.fillStyle = '#991b1b';
    ctx.fillText('Low/Out-of-the-money', 110, 15);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new BlackScholesPricer();
});