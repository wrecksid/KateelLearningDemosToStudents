// Financial Contagion Model - Network Simulation

class ContagionModel {
  constructor() {
    this.nodes = [];
    this.edges = [];
    this.defaulted = new Set();
    
    this.init();
  }

  init() {
    document.getElementById('run-sim').addEventListener('click', () => this.runSimulation());
    ['network-size', 'conn-prob', 'init-defaults'].forEach(id => {
      document.getElementById(id).addEventListener('input', (e) => {
        document.getElementById(`${id === 'conn-prob' ? 'prob' : id === 'init-defaults' ? 'default' : id}-val`).textContent = e.target.value;
      });
    });
    
    this.runSimulation();
  }

  runSimulation() {
    const size = parseInt(document.getElementById('network-size').value);
    const prob = parseInt(document.getElementById('conn-prob').value) / 100;
    const initDefaults = parseInt(document.getElementById('init-defaults').value);
    
    // Create network
    this.nodes = Array.from({ length: size }, (_, i) => ({ id: i, defaulted: false }));
    this.edges = [];
    
    for (let i = 0; i < size; i++) {
      for (let j = i + 1; j < size; j++) {
        if (Math.random() < prob / 100) {
          this.edges.push({ from: i, to: j });
        }
      }
    }
    
    // Initial defaults
    this.defaulted.clear();
    for (let i = 0; i < initDefaults; i++) {
      this.defaulted.add(i);
    }
    
    // Propagate (simplified)
    let changed = true;
    while (changed) {
      changed = false;
      this.edges.forEach(edge => {
        if (!this.defaulted.has(edge.from) || !this.defaulted.has(edge.to)) return;
        const neighbor = this.defaulted.has(edge.from) ? edge.to : edge.from;
        if (!this.defaulted.has(neighbor) && Math.random() < 0.3) {
          this.defaulted.add(neighbor);
          changed = true;
        }
      });
    }
    
    // Update UI
    document.getElementById('total-nodes').textContent = size;
    document.getElementById('defaulted').textContent = this.defaulted.size;
    document.getElementById('contagion').textContent = ((this.defaulted.size / size) * 100).toFixed(1) + '%';
    document.getElementById('threshold').textContent = '0.3';
    
    this.drawNetwork();
  }

  drawNetwork() {
    const canvas = document.getElementById('network-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 20;
    
    this.nodes.forEach((node, i) => {
      const angle = (i / this.nodes.length) * Math.PI * 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = this.defaulted.has(node.id) ? '#ef4444' : '#10b981';
      ctx.fill();
    });
    
    // Draw edges
    ctx.strokeStyle = '#e2e8f0';
    this.edges.forEach(edge => {
      const a = edge.from / this.nodes.length * Math.PI * 2;
      const b = edge.to / this.nodes.length * Math.PI * 2;
      const x1 = centerX + radius * Math.cos(a);
      const y1 = centerY + radius * Math.sin(a);
      const x2 = centerX + radius * Math.cos(b);
      const y2 = centerY + radius * Math.sin(b);
      
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new ContagionModel();
});