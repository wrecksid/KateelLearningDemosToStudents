// AI Feature Impact - Prioritize features by business impact
const form = document.getElementById('featureForm');
const matrixEl = document.getElementById('matrix');

let features = JSON.parse(localStorage.getItem('aiFeatures') || '[]');

function renderMatrix() {
  matrixEl.innerHTML = `
    <div class="matrix-header">Feature</div>
    <div class="matrix-header">Impact</div>
    <div class="matrix-header">Effort</div>
    <div class="matrix-header">Priority</div>
  `;
  
  features.sort((a, b) => (b.impact / b.effort) - (a.impact / a.effort)).forEach(f => {
    const priority = (f.impact / f.effort * 10).toFixed(1);
    const div = document.createElement('div');
    div.className = 'matrix-header';
    div.innerHTML = `
      <div>${f.name}</div>
      <div>${f.impact}</div>
      <div>${f.effort}</div>
      <div><strong>${priority}</strong></div>
    `;
    matrixEl.appendChild(div);
  });
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const feature = {
    name: document.getElementById('name').value,
    impact: parseInt(document.getElementById('impact').value),
    effort: parseInt(document.getElementById('effort').value)
  };
  features.push(feature);
  localStorage.setItem('aiFeatures', JSON.stringify(features));
  form.reset();
  document.getElementById('impactVal').textContent = '5';
  document.getElementById('effortVal').textContent = '5';
  renderMatrix();
});

renderMatrix();