// Aircraft IoT Intrusion Detection System
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const connectionsTable = document.getElementById('connectionsTable');
const alertsList = document.getElementById('alertsList');

const devices = ['Cockpit', 'Engines', 'Avionics', 'Sensors', 'Comms'];
const protocols = ['TCP', 'UDP', 'CAN', 'ARINC'];

function generateConnections() {
  const rows = [];
  for (let i = 0; i < 8; i++) {
    const device = devices[Math.floor(Math.random() * devices.length)];
    const protocol = protocols[Math.floor(Math.random() * protocols.length)];
    const ip = `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`;
    const status = Math.random() > 0.9 ? 'Suspicious' : 'Normal';
    rows.push({ device, protocol, ip, status });
  }
  return rows;
}

function renderConnections() {
  const connections = generateConnections();
  let html = '<table><thead><tr><th>Device</th><th>Protocol</th><th>IP Address</th><th>Status</th></tr></thead><tbody>';
  connections.forEach(c => {
    html += `<tr><td>${c.device}</td><td>${c.protocol}</td><td>${c.ip}</td><td class="${c.status === 'Suspicious' ? 'status-critical' : ''}">${c.status}</td></tr>`;
  });
  html += '</tbody></table>';
  connectionsTable.innerHTML = html;
}

function generateAlerts() {
  const alerts = [
    { id: 1, msg: 'Unusual CAN bus traffic detected', severity: 'critical', time: '14:32:15' },
    { id: 2, msg: 'Multiple failed login attempts on cockpit system', severity: 'warning', time: '14:31:42' },
    { id: 3, msg: 'Sensor data anomaly detected', severity: 'warning', time: '14:30:05' }
  ];
  return alerts;
}

function renderAlerts() {
  const alerts = generateAlerts();
  let html = '';
  alerts.forEach(a => {
    html += `<div class="alert-item ${a.severity}"><strong>${a.msg}</strong><div class="time">${a.time}</div></div>`;
  });
  alertsList.innerHTML = html;
}

function updateStatus() {
  const hasCritical = Math.random() > 0.7;
  if (hasCritical) {
    statusIndicator.className = 'status-dot status-critical';
    statusText.textContent = 'ALERT: Suspicious Activity Detected';
    statusText.className = '';
  } else {
    statusIndicator.className = 'status-dot status-secure';
    statusText.textContent = 'System Secure';
  }
}

setInterval(() => {
  renderConnections();
  renderAlerts();
  updateStatus();
}, 3000);

renderConnections();
renderAlerts();
updateStatus();