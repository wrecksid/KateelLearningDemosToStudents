// QFD Demo - Quality Function Deployment for AI Features

class QFDDemo {
  constructor() {
    this.customerRequirements = [
      "Accurate predictions",
      "Fast response time",
      "Easy to use interface",
      "Explainable results",
      "Robust to outliers"
    ];
    
    this.technicalRequirements = [
      "ML model integration",
      "API optimization",
      "UI/UX design",
      "Explainability module",
      "Anomaly detection"
    ];
    
    this.init();
  }

  init() {
    this.renderCRList();
    this.renderTRList();
    this.renderMatrix();
    
    document.getElementById('add-cr').addEventListener('click', () => this.addCR());
    document.getElementById('add-tr').addEventListener('click', () => this.addTR());
  }

  renderCRList() {
    const container = document.getElementById('cr-list');
    container.innerHTML = this.customerRequirements.map((cr, i) => `
      <div class="item">
        <input type="text" value="${cr}" data-index="${i}" onchange="app.updateCR(this)">
        <span onclick="app.removeCR(${i})" style="cursor: pointer; color: #ef4444;">×</span>
      </div>
    `).join('');
  }

  renderTRList() {
    const container = document.getElementById('tr-list');
    container.innerHTML = this.technicalRequirements.map((tr, i) => `
      <div class="item">
        <input type="text" value="${tr}" data-index="${i}" onchange="app.updateTR(this)">
        <span onclick="app.removeTR(${i})" style="cursor: pointer; color: #ef4444;">×</span>
      </div>
    `).join('');
  }

  renderMatrix() {
    const container = document.getElementById('matrix-container');
    let html = '<table class="matrix"><thead><tr><th></th>';
    
    this.technicalRequirements.forEach(tr => {
      html += `<th>${tr.substring(0, 15)}...</th>`;
    });
    html += '</tr></thead><tbody>';
    
    this.customerRequirements.forEach((cr, i) => {
      html += `<tr><td><strong>${cr.substring(0, 15)}...</strong></td>`;
      this.technicalRequirements.forEach((_, j) => {
        const score = this.calculateScore(i, j);
        html += `<td class="score ${score}" onclick="app.setScore(${i}, ${j})">${score.toUpperCase()}</td>`;
      });
      html += '</tr>';
    });
    html += '</tbody></table>';
    
    container.innerHTML = html;
    this.calculatePriority();
  }

  calculateScore(crIndex, trIndex) {
    // Simple mapping: diagonal items are high priority
    // Off-diagonal items have lower scores
    if (crIndex === trIndex) return 'high';
    if (Math.abs(crIndex - trIndex) === 1) return 'medium';
    return 'low';
  }

  setScore(crIndex, trIndex) {
    // Cycle through scores
    const current = this.calculateScore(crIndex, trIndex);
    let newScore = 'low';
    if (current === 'low') newScore = 'high';
    else if (current === 'high') newScore = 'medium';
    
    // In a real app, you'd store this in a 2D array
    this.calculatePriority();
  }

  calculatePriority() {
    // Calculate priority scores for each TR
    const priorities = this.technicalRequirements.map((_, trIndex) => {
      let score = 0;
      this.customerRequirements.forEach((_, crIndex) => {
        score += trIndex === crIndex ? 9 : trIndex === crIndex - 1 || trIndex === crIndex + 1 ? 3 : 1;
      });
      return { tr: this.technicalRequirements[trIndex], score };
    });
    
    priorities.sort((a, b) => b.score - a.score);
    
    const container = document.getElementById('priority-results');
    container.innerHTML = '<h3>Prioritized Features</h3>' + 
      priorities.map((p, i) => `
        <div class="priority-item">
          <div class="priority-rank ${i < 2 ? 'top' : i < 4 ? 'mid' : 'bottom'}">#${i + 1}</div>
          <span>${p.tr}</span>
          <span>Score: ${p.score}</span>
        </div>
      `).join('');
  }

  addCR() {
    const input = document.getElementById('new-cr');
    if (input.value.trim()) {
      this.customerRequirements.push(input.value.trim());
      this.renderCRList();
      this.renderMatrix();
      input.value = '';
    }
  }

  addTR() {
    const input = document.getElementById('new-tr');
    if (input.value.trim()) {
      this.technicalRequirements.push(input.value.trim());
      this.renderTRList();
      this.renderMatrix();
      input.value = '';
    }
  }

  removeCR(index) {
    this.customerRequirements.splice(index, 1);
    this.renderCRList();
    this.renderMatrix();
  }

  removeTR(index) {
    this.technicalRequirements.splice(index, 1);
    this.renderTRList();
    this.renderMatrix();
  }

  updateCR(element) {
    const index = parseInt(element.dataset.index);
    this.customerRequirements[index] = element.value;
    this.calculatePriority();
  }

  updateTR(element) {
    const index = parseInt(element.dataset.index);
    this.technicalRequirements[index] = element.value;
    this.calculatePriority();
  }
}

// Global app instance
let app;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  app = new QFDDemo();
});