// AI Risk Calculator - Risk assessment for AI projects
const sliders = document.querySelectorAll('input[type="range"]');
const riskLevelEl = document.getElementById('riskLevel');
const riskScoreEl = document.getElementById('riskScore');
const techRiskEl = document.getElementById('techRisk');
const opRiskEl = document.getElementById('opRisk');
const compRiskEl = document.getElementById('compRisk');

function calculateRisk() {
  const mc = parseInt(document.getElementById('modelComplexity').value);
  const dq = parseInt(document.getElementById('dataQuality').value);
  const rp = parseInt(document.getElementById('regulatoryPressure').value);
  const is = parseInt(document.getElementById('impactScore').value);

  // Technical risk: model complexity + data quality
  const techRisk = Math.round((mc * 0.6 + (10 - dq) * 0.4));
  
  // Operational risk: business impact + complexity
  const opRisk = Math.round((is * 0.7 + mc * 0.3));
  
  // Compliance risk: regulatory pressure + business impact
  const compRisk = Math.round((rp * 0.6 + is * 0.4));
  
  // Overall risk
  const overallRisk = Math.round((techRisk + opRisk + compRisk) / 3);
  
  // Update display
  riskScoreEl.textContent = overallRisk;
  techRiskEl.textContent = techRisk;
  opRiskEl.textContent = opRisk;
  compRiskEl.textContent = compRisk;
  
  // Determine risk level
  let level, className;
  if (overallRisk < 40) {
    level = 'Low';
    className = 'low';
  } else if (overallRisk < 70) {
    level = 'Medium';
    className = 'medium';
  } else {
    level = 'High';
    className = 'high';
  }
  
  riskLevelEl.textContent = level;
  riskLevelEl.className = className;
}

sliders.forEach(slider => {
  slider.addEventListener('input', function() {
    document.getElementById(this.id + 'Value').textContent = this.value;
    calculateRisk();
  });
});

// Initialize
calculateRisk();