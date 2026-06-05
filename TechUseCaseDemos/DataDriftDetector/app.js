// Data Drift Detector - Monitor input data distribution changes
const refChart = document.getElementById('refChart');
const curChart = document.getElementById('curChart');
const alertBox = document.getElementById('alertBox');
const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');

let isRunning = false;
let driftInterval = null;

// Generate normal distribution data
function generateData(mean, stdDev, count) {
  const data = [];
  for (let i = 0; i < count; i++) {
    let x = mean;
    let y = 0;
    for (let j = 0; j < 12; j++) {
      x += (Math.random() - 0.5) * stdDev;
      y += (Math.random() - 0.5) * stdDev;
    }
    data.push(x + y);
  }
  return data;
}

// Draw histogram
function drawHistogram(canvas, data, color) {
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const bins = 20;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const binSize = (max - min) / bins;
  const counts = new Array(bins).fill(0);
  
  data.forEach(v => {
    const bin = Math.min(Math.floor((v - min) / binSize), bins - 1);
    counts[bin]++;
  });
  
  const maxCount = Math.max(...counts);
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = color;
  
  counts.forEach((count, i) => {
    const barWidth = width / bins - 2;
    const barHeight = (count / maxCount) * (height - 30);
    ctx.fillRect(i * (barWidth + 2), height - barHeight - 20, barWidth, barHeight);
  });
}

// Calculate drift score (simplified PSI-like metric)
function calculateDrift(ref, cur) {
  const bins = 20;
  const all = [...ref, ...cur];
  const min = Math.min(...all);
  const max = Math.max(...all);
  const binSize = (max - min) / bins;
  
  const refBins = new Array(bins).fill(0);
  const curBins = new Array(bins).fill(0);
  
  ref.forEach(v => refBins[Math.min(Math.floor((v - min) / binSize), bins - 1)]++);
  cur.forEach(v => curBins[Math.min(Math.floor((v - min) / binSize), bins - 1)]++);
  
  let drift = 0;
  for (let i = 0; i < bins; i++) {
    const r = refBins[i] / ref.length;
    const c = curBins[i] / cur.length;
    drift += (c - r) * Math.log(c / (r + 0.0001) + 0.0001);
  }
  return Math.abs(drift);
}

let refData = generateData(50, 10, 1000);
let curData = [...refData];

function update() {
  curData = generateData(50 + Math.sin(Date.now() / 5000) * 15, 10, 1000);
  drawHistogram(refChart, refData, '#3b82f6');
  drawHistogram(curChart, curData, '#fbbf24');
  
  const drift = calculateDrift(refData, curData);
  alertBox.textContent = `Drift Score: ${drift.toFixed(2)}`;
  alertBox.style.background = drift > 0.2 ? 
    'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)' : 
    'linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%)';
}

startBtn.addEventListener('click', () => {
  if (isRunning) return;
  isRunning = true;
  driftInterval = setInterval(update, 1000);
});

resetBtn.addEventListener('click', () => {
  isRunning = false;
  clearInterval(driftInterval);
  curData = [...refData];
  update();
});

// Initialize
drawHistogram(refChart, refData, '#3b82f6');
drawHistogram(curChart, curData, '#fbbf24');
alertBox.textContent = 'Drift Score: 0.00';