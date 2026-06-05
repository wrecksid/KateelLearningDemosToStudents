// Aircraft IoT Vulnerability Scanner
const targetEl = document.getElementById('target');
const resultsEl = document.getElementById('scanResults');

const vulnDatabase = {
  cockpit: [
    { id: 'CVE-2023-1234', name: 'Flight Control Buffer Overflow', severity: 'critical', desc: 'Buffer overflow in flight control firmware' },
    { id: 'CVE-2023-5678', name: 'Authentication Bypass', severity: 'high', desc: 'Weak authentication in cockpit UI' }
  ],
  engines: [
    { id: 'CVE-2023-9012', name: 'CAN Bus Injection', severity: 'critical', desc: 'Unsanitized CAN bus commands' },
    { id: 'CVE-2023-3456', name: 'Telemetry Exposure', severity: 'medium', desc: 'Unencrypted engine telemetry' }
  ],
  avionics: [
    { id: 'CVE-2023-7890', name: 'ARINC Weak Encryption', severity: 'high', desc: 'ARINC 429 lacks encryption' },
    { id: 'CVE-2023-2345', name: 'GPS Spoofing', severity: 'high', desc: 'GPS signals not validated' }
  ],
  sensors: [
    { id: 'CVE-2023-4567', name: 'Sensor Tampering', severity: 'medium', desc: 'No integrity checks on sensor data' }
  ],
  comms: [
    { id: 'CVE-2023-8901', name: 'Radio Protocol Flaw', severity: 'high', desc: 'HF radio encryption weakness' }
  ]
};

function startScan() {
  resultsEl.innerHTML = '<div class="card"><p>Scanning...</p></div>';
  const target = targetEl.value;
  
  setTimeout(() => {
    const vulns = vulnDatabase[target] || [];
    let html = '';
    vulns.forEach(v => {
      html += `
        <div class="vuln-card ${v.severity}">
          <h4>${v.name} (${v.id})</h4>
          <p>${v.desc}</p>
          <div class="meta">Severity: ${v.severity.toUpperCase()}</div>
        </div>
      `;
    });
    if (html === '') html = '<div class="card"><p>No vulnerabilities found</p></div>';
    resultsEl.innerHTML = html;
  }, 1500);
}

startScan();