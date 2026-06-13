// AI Performance Dashboard - Monitor model metrics and KPIs
const canvas = document.getElementById('latencyChart');
const ctx = canvas.getContext('2d');

// Simple bar chart using canvas
function drawChart() {
  const data = [5, 10, 25, 40, 60, 80, 95, 100, 90, 70, 45, 20];
  const labels = ['0-2ms', '2-5ms', '5-10ms', '10-20ms', '20-50ms', '50-100ms', '100-200ms', '200-500ms', '500ms-1s', '1-2s', '2-5s', '5s+'];
  
  const width = ctx.width;
  const height = ctx.height;
  const barWidth = width / data.length - 4;
  const maxCount = Math.max(...data);
  
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = '#3b82f6';
  
  data.forEach((val, i) => {
    const barHeight = (val / maxCount) * (height - 40);
    ctx.fillRect(i * (barWidth + 4) + 2, height - barHeight - 20, barWidth, barHeight);
  });
  
  // Labels
  ctx.fillStyle = '#94a3b8';
  ctx.font = '10px sans-serif';
  labels.forEach((label, i) => {
    ctx.fillText(label, i * (barWidth + 4) + 2, height - 10);
  });
}

// Simulate real-time updates
setInterval(() => {
  document.getElementById('accuracy').textContent = (94 + Math.random() * 1.5).toFixed(1) + '%';
  document.getElementById('precision').textContent = (92 + Math.random() * 2).toFixed(1) + '%';
  document.getElementById('recall').textContent = (91 + Math.random() * 2.5).toFixed(1) + '%';
  document.getElementById('f1').textContent = (91.5 + Math.random() * 1).toFixed(1) + '%';
}, 2000);

drawChart();