// AI Team Collaboration - RACI matrix for AI projects
const form = document.getElementById('memberForm');
const matrixEl = document.getElementById('matrix');

let members = JSON.parse(localStorage.getItem('aiTeamMembers') || '[]');

function renderMatrix() {
  matrixEl.innerHTML = '';
  members.forEach(m => {
    const card = document.createElement('div');
    card.className = 'member-card';
    card.innerHTML = `
      <div>
        <strong>${m.name}</strong>
        <div style="font-size: 0.75rem; color: #fca5a5;">${m.role}</div>
      </div>
      <div style="font-size: 0.875rem;">${m.responsibilities.join(', ')}</div>
    `;
    matrixEl.appendChild(card);
  });
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const role = document.getElementById('role').value;
  const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
  const responsibilities = Array.from(checkboxes).map(cb => cb.value);
  
  members.push({ name, role, responsibilities });
  localStorage.setItem('aiTeamMembers', JSON.stringify(members));
  form.reset();
  renderMatrix();
});

renderMatrix();