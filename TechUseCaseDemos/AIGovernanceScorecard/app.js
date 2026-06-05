// AI Governance Scorecard - Assess AI ethics and compliance
const checklistEl = document.getElementById('checklist');
const scoreValueEl = document.getElementById('scoreValue');
const scoreStatusEl = document.getElementById('scoreStatus');

const items = [
  { id: 'fairness', text: 'Fairness and Bias Mitigation' },
  { id: 'transparency', text: 'Model Transparency/Explainability' },
  { id: 'privacy', text: 'Privacy Protection (GDPR/CCPA)' },
  { id: 'safety', text: 'Safety and Security Measures' },
  { id: 'audit', text: 'Audit Trail and Documentation' },
  { id: 'validation', text: 'Model Validation and Testing' },
  { id: 'monitoring', text: 'Ongoing Monitoring Plan' },
  { id: 'governance', text: 'Governance Committee' }
];

let checked = new Set(JSON.parse(localStorage.getItem('governanceChecks') || '[]'));

function renderChecklist() {
  checklistEl.innerHTML = '';
  items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'checklist-item';
    div.innerHTML = `
      <input type="checkbox" id="${item.id}" ${checked.has(item.id) ? 'checked' : ''}>
      <label for="${item.id}">${item.text}</label>
    `;
    const cb = div.querySelector('input');
    cb.addEventListener('change', () => {
      if (cb.checked) checked.add(item.id);
      else checked.delete(item.id);
      localStorage.setItem('governanceChecks', JSON.stringify([...checked]));
      updateScore();
    });
    checklistEl.appendChild(div);
  });
}

function updateScore() {
  const score = Math.round((checked.size / items.length) * 100);
  scoreValueEl.textContent = score;
  scoreValueEl.className = 'score-value';
  if (score < 40) {
    scoreValueEl.classList.add('low');
    scoreStatusEl.textContent = 'High Risk';
    scoreStatusEl.className = 'score-status low';
  } else if (score < 70) {
    scoreValueEl.classList.add('medium');
    scoreStatusEl.textContent = 'Medium Risk';
    scoreStatusEl.className = 'score-status medium';
  } else {
    scoreValueEl.classList.add('high');
    scoreStatusEl.textContent = 'Compliant';
    scoreStatusEl.className = 'score-status high';
  }
}

renderChecklist();
updateScore();