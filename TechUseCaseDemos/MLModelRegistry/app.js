// ML Model Registry - Version and track machine learning models
const form = document.getElementById('modelForm');
const registryEl = document.getElementById('registry');

function loadModels() {
  const models = JSON.parse(localStorage.getItem('mlModels') || '[]');
  renderRegistry(models);
}

function renderRegistry(models) {
  registryEl.innerHTML = '';
  models.forEach(m => {
    const div = document.createElement('div');
    div.className = 'model-card';
    div.innerHTML = `
      <div>
        <h3>${m.name}</h3>
        <div class="meta">Framework: ${m.framework} | Accuracy: ${m.accuracy}%</div>
      </div>
      <div>
        <span class="version">v${m.version}</span>
      </div>
    `;
    registryEl.appendChild(div);
  });
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const model = {
    name: document.getElementById('name').value,
    version: document.getElementById('version').value,
    framework: document.getElementById('framework').value,
    accuracy: parseFloat(document.getElementById('accuracy').value)
  };
  const models = JSON.parse(localStorage.getItem('mlModels') || '[]');
  models.unshift(model);
  localStorage.setItem('mlModels', JSON.stringify(models));
  form.reset();
  document.getElementById('accuracy').value = '95.0';
  renderRegistry(models);
});

loadModels();