// Aircraft IoT Threat Modeling Matrix - STRIDE analysis
const threatGrid = document.getElementById('threatGrid');
const threatForm = document.getElementById('threatForm');
const threatList = document.getElementById('threatList');

const categories = ['Spoofing', 'Tampering', 'Repudiation', 'Information Disclosure', 'Denial of Service', 'Elevation of Privilege'];
const assets = ['Flight Controls', 'Engine Systems', 'Navigation', 'Communications', 'Passenger Data'];

let threats = JSON.parse(localStorage.getItem('aircraftThreats') || '[]');

function renderCategories() {
  categories.forEach(cat => {
    const card = document.createElement('div');
    card.className = `threat-card ${cat === 'Spoofing' ? 'spoofing' : cat === 'Tampering' ? 'tampering' : cat === 'Information Disclosure' ? 'info' : cat === 'Denial of Service' ? 'dos' : ''}`;
    card.innerHTML = `<h4>${cat}</h4><div class="risk">${threats.filter(t => t.category === cat).length} threats</div>`;
    threatGrid.appendChild(card);
  });
}

function renderThreats() {
  threatList.innerHTML = '';
  threats.forEach((t, i) => {
    const div = document.createElement('div');
    div.className = 'threat-item';
    div.innerHTML = `
      <div>
        <strong>${t.category}</strong> - ${t.asset}
        <div style="font-size: 0.875rem; color: var(--text-secondary);">${t.description || ''}</div>
      </div>
      <span class="badge badge-${t.risk}">${t.risk.toUpperCase()}</span>
    `;
    threatList.appendChild(div);
  });
}

threatForm.addEventListener('submit', e => {
  e.preventDefault();
  const threat = {
    category: document.getElementById('category').value,
    asset: document.getElementById('asset').value,
    risk: document.getElementById('risk').value,
    description: '',
    date: new Date().toISOString().slice(0, 10)
  };
  threats.push(threat);
  localStorage.setItem('aircraftThreats', JSON.stringify(threats));
  threatForm.reset();
  renderThreats();
});

renderCategories();
renderThreats();