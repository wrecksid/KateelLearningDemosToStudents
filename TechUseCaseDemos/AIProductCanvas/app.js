// AI Product Canvas - Product Planning Tool

class AIProductCanvas {
  constructor() {
    this.sections = ['problem', 'solution', 'users', 'data', 'metrics', 'tradeoffs', 'ethics', 'mvp'];
    this.init();
  }

  init() {
    // Load saved data
    this.load();

    // Bind events
    document.getElementById('save-btn').addEventListener('click', () => this.save());
    document.getElementById('export-btn').addEventListener('click', () => this.export());

    // Add change listeners to all textareas
    document.querySelectorAll('.canvas-card textarea').forEach(ta => {
      ta.addEventListener('change', () => this.save());
    });
  }

  save() {
    const data = {};
    this.sections.forEach(section => {
      const textarea = document.querySelector(`[data-section="${section}"] textarea`);
      data[section] = textarea.value;
    });
    localStorage.setItem('aiProductCanvas', JSON.stringify(data));
  }

  load() {
    const saved = localStorage.getItem('aiProductCanvas');
    if (saved) {
      const data = JSON.parse(saved);
      this.sections.forEach(section => {
        const textarea = document.querySelector(`[data-section="${section}"] textarea`);
        if (textarea && data[section]) {
          textarea.value = data[section];
        }
      });
    }
  }

  export() {
    const data = {};
    this.sections.forEach(section => {
      const textarea = document.querySelector(`[data-section="${section}"] textarea`);
      data[section] = textarea.value;
    });

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-product-canvas.json';
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new AIProductCanvas();
});