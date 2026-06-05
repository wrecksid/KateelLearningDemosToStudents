// NPV Calculator - Capital Budgeting Analysis
// Calculates Net Present Value and Internal Rate of Return

class NPVCalculator {
    constructor() {
        this.init();
    }
    
    init() {
        document.getElementById('calculate-btn').addEventListener('click', () => this.calculate());
        this.calculate();
    }
    
    calculate() {
        const cashFlowText = document.getElementById('cashflows').value;
        const rate = parseFloat(document.getElementById('discount').value) / 100;
        
        const cashflows = cashFlowText.split('\n')
            .map(line => parseFloat(line.trim()))
            .filter(n => !isNaN(n));
        
        // Calculate NPV
        let npv = 0;
        let pvTotal = 0;
        
        cashflows.forEach((cf, i) => {
            const pv = cf / Math.pow(1 + rate, i);
            npv += pv;
            pvTotal += Math.abs(pv);
        });
        
        // Initial investment (first negative cashflow)
        const initial = cashflows[0] < 0 ? Math.abs(cashflows[0]) : 0;
        npv -= initial;
        
        // Calculate IRR (simple approximation)
        const irr = this.calculateIRR(cashflows, rate);
        
        // Update UI
        document.getElementById('npv').textContent = '$' + npv.toFixed(2);
        document.getElementById('irr').textContent = irr.toFixed(1) + '%';
        document.getElementById('pv').textContent = '$' + pvTotal.toFixed(2);
    }
    
    calculateIRR(cashflows, guess = 0.1) {
        let rate = guess;
        const tolerance = 0.0001;
        const maxIterations = 100;
        
        for (let i = 0; i < maxIterations; i++) {
            let npv = 0;
            cashflows.forEach((cf, j) => {
                npv += cf / Math.pow(1 + rate, j);
            });
            
            if (Math.abs(npv) < tolerance) break;
            
            // Newton's method approximation
            let derivative = 0;
            cashflows.forEach((cf, j) => {
                if (j > 0) derivative -= j * cf / Math.pow(1 + rate, j + 1);
            });
            
            rate = rate - npv / (derivative || 0.001);
        }
        
        return rate * 100;
    }
}

document.addEventListener('DOMContentLoaded', () => new NPVCalculator());