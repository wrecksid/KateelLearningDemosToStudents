// AI Resource Planner - Estimate compute resources and costs
const modelTypeEl = document.getElementById('modelType');
const volumeEl = document.getElementById('inferenceVolume');
const latencyEl = document.getElementById('latency');
const durationEl = document.getElementById('duration');
const computeEl = document.getElementById('compute');
const memoryEl = document.getElementById('memory');
const storageEl = document.getElementById('storage');
const monthlyCostEl = document.getElementById('monthlyCost');
const totalCostEl = document.getElementById('totalCost');

function calculateResources() {
  const modelType = modelTypeEl.value;
  const volume = parseInt(volumeEl.value) || 0;
  const latency = parseInt(latencyEl.value) || 100;
  const duration = parseInt(durationEl.value) || 12;

  // Base resource estimates (simplified)
  const base = {
    small: { cpu: '2 vCPU', ram: '4 GB', storage: '10 GB', cost: 50 },
    medium: { cpu: '4 vCPU', ram: '16 GB', storage: '100 GB', cost: 200 },
    large: { cpu: '8 vCPU', ram: '64 GB', storage: '500 GB', cost: 800 },
    custom: { cpu: '4 vCPU', ram: '32 GB', storage: '250 GB', cost: 400 }
  };

  const b = base[modelType];
  
  // Scale by volume
  const scaleFactor = Math.max(1, Math.log10(volume / 1000 + 1));
  
  // Adjust for latency requirements
  const latencyFactor = latency < 50 ? 2 : latency < 100 ? 1.5 : 1;

  const finalCpu = modelType === 'small' ? b.cpu : `${Math.round(parseInt(b.cpu) * scaleFactor * latencyFactor)} vCPU`;
  const finalRam = `${Math.round(parseInt(b.ram) * scaleFactor * latencyFactor)} GB`;
  const finalStorage = `${Math.round(parseInt(b.storage) * scaleFactor)} GB`;
  
  const hourlyCost = b.cost * scaleFactor * latencyFactor;
  const monthlyCost = hourlyCost * 24 * 30 / 1000;
  const totalCost = monthlyCost * duration;

  computeEl.textContent = finalCpu;
  memoryEl.textContent = finalRam;
  storageEl.textContent = finalStorage;
  monthlyCostEl.textContent = `$${monthlyCost.toFixed(2)}`;
  totalCostEl.textContent = `$${totalCost.toFixed(2)}`;
}

modelTypeEl.addEventListener('change', calculateResources);
volumeEl.addEventListener('input', calculateResources);
latencyEl.addEventListener('input', calculateResources);
durationEl.addEventListener('input', calculateResources);

calculateResources();