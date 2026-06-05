// AI Regulatory Tracker - Track compliance requirements and deadlines
const form = document.getElementById('regForm');
const regListEl = document.getElementById('regList');

let regulations = JSON.parse(localStorage.getItem('aiRegulations') || '[]');

function renderRegulations() {
  regListEl.innerHTML = '';
  regulations.sort((a, b) => new Date(a.deadline) - new Date(b.deadline)).forEach(r => {
    const days = Math.ceil((new Date(r.deadline) - new Date()) / (1000 * 60 * 60 * 24));
    const item = document.createElement('div');
    item.className = 'reg-item';
    item.innerHTML = `
      <strong>${r.name}</strong>
      <div class="jurisdiction">${r.jurisdiction} • Due: ${r.deadline} (${days > 0 ? days + ' days' : 'overdue'})</div>
      <div style="margin-top: 0.25rem;">Status: <strong>${r.status}</strong></div>
    `;
    regListEl.appendChild(item);
  });
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const reg = {
    name: document.getElementById('name').value,
    jurisdiction: document.getElementById('jurisdiction').value,
    deadline: document.getElementById('deadline').value,
    status: document.getElementById('status').value
  };
  regulations.push(reg);
  localStorage.setItem('aiRegulations', JSON.stringify(regulations));
  form.reset();
  renderRegulations();
});

renderRegulations();