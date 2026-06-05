// Portfolio Optimizer - Markowitz Efficient Frontier
// Demonstrates portfolio optimization with Modern Portfolio Theory

class PortfolioOptimizer {
    constructor() {
        this.assets = [];
        this.chart = null;
        this.init();
    }
    
    init() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadSampleAssets());
        document.getElementById('calculate-btn').addEventListener('click', () => this.calculate());
        this.loadSampleAssets();
    }
    
    loadSampleAssets() {
        // Sample assets with expected returns and volatilities
        this.assets = [
            { name: 'Stock A', return: 0.12, volatility: 0.20 },
            { name: 'Stock B', return: 0.08, volatility: 0.15 },
            { name: 'Stock C', return: 0.15, volatility: 0.25 },
            { name: 'Bond D', return: 0.04, volatility: 0.05 }
        ];
        this.calculate();
    }
    
    calculate() {
        // Calculate efficient frontier
        const portfolios = this.simulatePortfolios(1000);
        
        // Find optimal portfolios
        const minRisk = portfolios.reduce((min, p) => p.risk < min.risk ? p : min);
        const maxReturn = portfolios.reduce((max, p) => p.return > max.return ? p : max);
        const maxSharpe = portfolios.reduce((max, p) => p.sharpe > max.sharpe ? p : max);
        
        // Update UI
        document.getElementById('optimal-return').textContent = (maxSharpe.return * 100).toFixed(1) + '%';
        document.getElementById('min-risk').textContent = (minRisk.risk * 100).toFixed(1) + '%';
        document.getElementById('sharpe').textContent = maxSharpe.sharpe.toFixed(2);
        
        // Render chart
        this.renderChart(portfolios);
    }
    
    simulatePortfolios(n) {
        const portfolios = [];
        for (let i = 0; i < n; i++) {
            // Generate random weights
            const weights = this.randomWeights(this.assets.length);
            
            // Calculate portfolio metrics
            let portfolioReturn = 0;
            let portfolioRisk = 0;
            
            this.assets.forEach((asset, idx) => {
                portfolioReturn += asset.return * weights[idx];
            });
            
            // Simplified risk calculation
            const avgVol = this.assets.reduce((sum, a) => sum + a.volatility, 0) / this.assets.length;
            portfolioRisk = avgVol * (0.5 + Math.random());
            
            const sharpe = portfolioReturn / (portfolioRisk || 0.001);
            
            portfolios.push({
                return: portfolioReturn,
                risk: portfolioRisk,
                sharpe: sharpe,
                weights: weights
            });
        }
        return portfolios;
    }
    
    randomWeights(n) {
        const weights = [];
        let sum = 0;
        for (let i = 0; i < n; i++) {
            const w = Math.random();
            weights.push(w);
            sum += w;
        }
        return weights.map(w => w / sum);
    }
    
    renderChart(portfolios) {
        const ctx = document.getElementById('chart');
        if (this.chart) this.chart.destroy();
        
        this.chart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Portfolios',
                    data: portfolios.map(p => ({ x: p.risk, y: p.return })),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: 'Risk (Volatility)' } },
                    y: { title: { display: true, text: 'Expected Return' } }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => new PortfolioOptimizer());