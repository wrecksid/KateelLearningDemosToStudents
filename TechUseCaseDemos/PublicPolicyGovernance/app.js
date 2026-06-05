// Public Policy Resource Allocation Lab
// AI-driven policy simulation and impact analysis

class PolicyLab {
    constructor() {
        this.budget = {
            education: 40,
            healthcare: 30,
            infrastructure: 20,
            social: 10
        };
        this.totalBudget = 100;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateAllValues();
    }

    bindEvents() {
        document.getElementById('run-simulation').addEventListener('click', () => this.runSimulation());
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());
        
        const sliders = ['education', 'healthcare', 'infrastructure', 'social'];
        sliders.forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => this.updateSlider(e));
        });
    }

    updateSlider(e) {
        const id = e.target.id;
        const value = e.target.value;
        this.budget[id] = parseInt(value);
        this.updateAllValues();
    }

    updateAllValues() {
        document.getElementById('edu-value').textContent = this.budget.education;
        document.getElementById('health-value').textContent = this.budget.healthcare;
        document.getElementById('infra-value').textContent = this.budget.infrastructure;
        document.getElementById('social-value').textContent = this.budget.social;
    }

    runSimulation() {
        const total = this.budget.education + this.budget.healthcare + 
                      this.budget.infrastructure + this.budget.social;
        
        const resultsEl = document.getElementById('results');
        
        if (total !== this.totalBudget) {
            resultsEl.innerHTML = `<p class="warning">⚠️ Budget must total 100% (currently ${total}%)</p>`;
            return;
        }

        // Calculate policy impacts (simplified model)
        const educationImpact = this.calculateEducationImpact();
        const healthImpact = this.calculateHealthImpact();
        const infraImpact = this.calculateInfrastructureImpact();
        const socialImpact = this.calculateSocialImpact();
        const equityScore = this.calculateEquity();

        resultsEl.innerHTML = `
            <div class="metric">
                <span class="label">Education Impact</span>
                <span class="value">${educationImpact.toFixed(1)}/100</span>
            </div>
            <div class="metric">
                <span class="label">Health Outcomes</span>
                <span class="value">${healthImpact.toFixed(1)}/100</span>
            </div>
            <div class="metric">
                <span class="label">Infrastructure Quality</span>
                <span class="value">${infraImpact.toFixed(1)}/100</span>
            </div>
            <div class="metric">
                <span class="label">Social Welfare</span>
                <span class="value">${socialImpact.toFixed(1)}/100</span>
            </div>
            <div class="metric">
                <span class="label">Equity Score</span>
                <span class="value ${equityScore > 70 ? 'success' : 'warning'}">${equityScore.toFixed(1)}/100</span>
            </div>
            <div class="metric">
                <span class="label">Overall Welfare</span>
                <span class="value success">${((educationImpact + healthImpact + infraImpact + socialImpact + equityScore) / 5).toFixed(1)}/100</span>
            </div>
        `;
    }

    calculateEducationImpact() {
        // Diminishing returns model
        return Math.min(100, this.budget.education * 1.5 + Math.sqrt(this.budget.education) * 2);
    }

    calculateHealthImpact() {
        return Math.min(100, this.budget.healthcare * 1.8 + Math.sqrt(this.budget.healthcare) * 1.5);
    }

    calculateInfrastructureImpact() {
        return Math.min(100, this.budget.infrastructure * 1.3 + this.budget.infrastructure);
    }

    calculateSocialImpact() {
        return Math.min(100, this.budget.social * 2.0 + Math.sqrt(this.budget.social) * 3);
    }

    calculateEquity() {
        // Higher social spending improves equity
        // More balanced allocation improves equity
        const balance = 100 - Math.abs(this.budget.education - 40) / 40 * 100 -
                             Math.abs(this.budget.healthcare - 30) / 30 * 100 -
                             Math.abs(this.budget.infrastructure - 20) / 20 * 100 -
                             Math.abs(this.budget.social - 10) / 10 * 100;
        return Math.max(0, balance * 0.7 + this.budget.social * 0.3);
    }

    reset() {
        this.budget = {
            education: 40,
            healthcare: 30,
            infrastructure: 20,
            social: 10
        };
        this.updateAllValues();
        document.getElementById('results').innerHTML = '<p>Set budget percentages and run simulation.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PolicyLab();
});