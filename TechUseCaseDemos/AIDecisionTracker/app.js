// AI Decision Tracker - Log and review AI product decisions
const form = document.getElementById('decisionForm');
const listEl = document.getElementById('decisionList');

function loadDecisions() {
  const decisions = JSON.parse(localStorage.getItem('aiDecisions') || '[]');
  renderDecisions(decisions);
}

function renderDecisions(decisions) {
  listEl.innerHTML = '';
  decisions.forEach(d => {
    const div = document.createElement('div');
    div.className = 'decision-item';
    div.innerHTML = `
      <div class="category">${d.category}</div>
      <div class="decision">${d.decision}</div>
      <div class="rationale">Why: ${d.rationale}</div>
      <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">${d.date}</div>
    `;
    listEl.appendChild(div);
  });
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const decision = document.getElementById('decision').value;
  const category = document.getElementById('category').value;
  const rationale = document.getElementById('rationale').value;
  
  const decisions = JSON.parse(localStorage.getItem('aiDecisions') || '[]');
  decisions.unshift({ decision, category, rationale, date: new Date().toISOString().slice(0, 10) });
  localStorage.setItem('aiDecisions', JSON.stringify(decisions));
  
  form.reset();
  renderDecisions(decisions);
});

loadDecisions();