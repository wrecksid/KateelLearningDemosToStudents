// AI Governance & Compliance Lab
// Public sector AI ethics and regulatory compliance assessment

class AIGovernanceLab {
    constructor() {
        this.requirements = {
            fairness: { name: 'Fairness & Bias Audit', weight: 0.25 },
            transparency: { name: 'Explainability Report', weight: 0.20 },
            privacy: { name: 'Data Privacy Impact', weight: 0.15 },
            human: { name: 'Human-in-the-Loop', weight: 0.15 },
            audit: { name: 'Audit Trail Ready', weight: 0.15 },
            redress: { name: 'Redress Mechanism', weight: 0.10 }
        };
        
        this.init();
    }

    init() {
        document.getElementById('assess-btn').addEventListener('click', () => this.assess());
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());
    }

    assess() {
        const systemName = document.getElementById('system-name').value || 'AI System';
        const useCase = document.getElementById('use-case').value;
        const riskLevel = document.getElementById('risk-level').value;
        
        const results = this.calculateScore();
        const resultsEl = document.getElementById('assessment-results');
        const panel = document.getElementById('results');
        
        panel.style.display = 'block';
        
        let html = `
            <div class="score-bar">
                <div class="score-header">
                    <span><strong>${systemName}</strong></span>
                    <span>${riskLevel.toUpperCase()} RISK</span>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill ${results.overall >= 80 ? 'score-pass' : results.overall >= 60 ? 'score-warn' : 'score-fail'}" style="width: ${results.overall}%"></div>
                </div>
            </div>
        `;
        
        for (const [key, req] of Object.entries(this.requirements)) {
            const checked = document.getElementById(key).checked;
            const score = checked ? req.weight * 100 : 0;
            const status = checked ? '✓' : '✗';
            const statusClass = checked ? 'score-pass' : 'score-fail';
            
            html += `
                <div class="score-bar">
                    <div class="score-header">
                        <span>${req.name}</span>
                        <span class="${statusClass}">${status} ${score.toFixed(0)}%</span>
                    </div>
                </div>
            `;
        }
        
        html += `
            <div class="score-bar" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                <div class="score-header">
                    <strong>Overall Compliance Score</strong>
                    <strong>${results.overall.toFixed(1)}%</strong>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill ${results.overall >= 80 ? 'score-pass' : results.overall >= 60 ? 'score-warn' : 'score-fail'}" style="width: ${results.overall}%"></div>
                </div>
            </div>
        `;
        
        if (results.recommendations.length > 0) {
            html += `
                <div style="margin-top: 15px; padding: 15px; background: rgba(245, 158, 11, 0.1); border-radius: 8px;">
                    <strong>Recommendations:</strong>
                    <ul style="margin: 10px 0 0 0; padding-left: 20px;">
            `;
            results.recommendations.forEach(rec => {
                html += `<li>${rec}</li>`;
            });
            html += '</ul></div>';
        }
        
        resultsEl.innerHTML = html;
    }

    calculateScore() {
        let total = 0;
        const completed = [];
        const recommendations = [];
        
        for (const [key, req] of Object.entries(this.requirements)) {
            const checked = document.getElementById(key).checked;
            if (checked) {
                total += req.weight * 100;
                completed.push(req.name);
            } else {
                recommendations.push(`Complete ${req.name} requirement`);
            }
        }
        
        const overall = total / Object.keys(this.requirements).length;
        
        return { overall, recommendations };
    }

    reset() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = false);
        document.getElementById('results').style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AIGovernanceLab();
});