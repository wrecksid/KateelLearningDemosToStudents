// Aircraft IoT Network Traffic Analyzer
const totalPacketsEl = document.getElementById('totalPackets');
const canTrafficEl = document.getElementById('canTraffic');
const arincTrafficEl = document.getElementById('arincTraffic');
const anomaliesEl = document.getElementById('anomalies');
const trafficLog = document.getElementById('trafficLog');
const ctx = document.getElementById('protocolChart');

let totalPackets = 0;
let canTraffic = 0;
let arincTraffic = 0;
let anomalies = 0;

function drawChart() {
  const labels = ['CAN Bus', 'ARINC', 'TCP', 'UDP'];
  const data = [canTraffic, arincTraffic, Math.floor(Math.random() * 1000), Math.floor(Math.random() * 500)];
  const colors = ['#0ea5e9', '#10b981', '#8b5cf6', '#f59e0b'];
  
  ctx.width = ctx.width || 400;
  const width = ctx.width;
  const height = ctx.height || 200;
  const barWidth = width / labels.length - 10;
  const maxVal = Math.max(...data, 1);
  
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = '#3b82f6';
  
  data.forEach((val, i) => {
    const barHeight = (val / maxVal) * (height - 40);
    ctx.fillStyle = colors[i];
    ctx.fillRect(i * (barWidth + 10) + 5, height - barHeight - 20, barWidth, barHeight);
  });
}

function updateStats() {
  totalPackets += Math.floor(Math.random() * 100);
  canTraffic += Math.random() > 0.7 ? Math.floor(Math.random() * 50) : 0;
  arincTraffic += Math.floor(Math.random() * 30);
  
  if (Math.random() > 0.95) anomalies++;
  
  totalPacketsEl.textContent = totalPackets.toLocaleString();
  canTrafficEl.textContent = canTraffic.toLocaleString();
  arincTrafficEl.textContent = arincTraffic.toLocaleString();
  anomaliesEl.textContent = anomalies;
  
  drawChart();
}

function updateLog() {
  const entries = ['CAN: Engine RPM=2400', 'ARINC: Alt=35000ft', 'TCP: ATC comms', 'UDP: Weather data'];
  const entry = entries[Math.floor(Math.random() * entries.length)];
  const div = document.createElement('div');
  div.style.padding = '0.5rem';
  div.style.background = 'rgba(255,255,255,0.05)';
  div.style.marginBottom = '0.25rem';
  div.style.borderRadius = '4px';
  div.textContent = `[${new Date().toLocaleTimeString()}] ${entry}`;
  trafficLog.prepend(div);
  if (trafficLog.children.length > 10) trafficLog.removeChild(trafficLog.lastChild);
}

setInterval(() => {
  updateStats();
  updateLog();
}, 1000);

updateStats();
drawChart();