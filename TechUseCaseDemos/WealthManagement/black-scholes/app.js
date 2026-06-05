// Black Scholes Options Pricer
// Calculates call and put option prices using the Black Scholes model

class BlackScholes {
    constructor() {
        this.init();
    }
    
    init() {
        document.getElementById('calculate-btn').addEventListener('click', () => this.calculate());
        this.calculate(); // Initial calculation
    }
    
    normCDF(x) {
        // Approximation of standard normal CDF
        const a1 =  0.254829592;
        const a2 = -0.284496736;
        const a3 =  1.421413741;
        const a4 = -1.453152027;
        const a5 =  1.061405429;
        const p  =  0.3275911;
        
        const sign = x < 0 ? -1 : 1;
        x = Math.abs(x) / Math.sqrt(2);
        
        const t = 1.0 / (1.0 + p * x);
        const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
        
        return 0.5 * (1.0 + sign * y);
    }
    
    calculate() {
        const S = parseFloat(document.getElementById('spot').value);
        const K = parseFloat(document.getElementById('strike').value);
        const T = parseFloat(document.getElementById('time').value);
        const r = parseFloat(document.getElementById('rate').value);
        const sigma = parseFloat(document.getElementById('vol').value);
        
        // Black Scholes calculation
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        const d2 = d1 - sigma * Math.sqrt(T);
        
        const call = S * this.normCDF(d1) - K * Math.exp(-r * T) * this.normCDF(d2);
        const put = K * Math.exp(-r * T) * this.normCDF(-d2) - S * this.normCDF(-d1);
        
        const deltaCall = this.normCDF(d1);
        const deltaPut = this.normCDF(d1) - 1;
        
        // Update UI
        document.getElementById('call-price').textContent = '$' + call.toFixed(2);
        document.getElementById('put-price').textContent = '$' + put.toFixed(2);
        document.getElementById('delta-call').textContent = deltaCall.toFixed(2);
        document.getElementById('delta-put').textContent = deltaPut.toFixed(2);
    }
}

document.addEventListener('DOMContentLoaded', () => new BlackScholes());