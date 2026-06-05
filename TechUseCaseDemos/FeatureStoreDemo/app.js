// Feature Store Demo - Central Feature Registry

class FeatureStore {
  constructor() {
    this.features = [
      { id: 'customer_age', name: 'Customer Age', type: 'customer', description: 'Customer age in years', dtype: 'int', freshness: 'daily' },
      { id: 'customer_income', name: 'Annual Income', type: 'customer', description: 'Customer annual income in USD', dtype: 'float', freshness: 'monthly' },
      { id: 'customer_credit_score', name: 'Credit Score', type: 'customer', description: 'FICO credit score', dtype: 'int', freshness: 'weekly' },
      { id: 'txn_amount', name: 'Transaction Amount', type: 'transaction', description: 'Amount of transaction', dtype: 'float', freshness: 'real-time' },
      { id: 'txn_merchant_category', name: 'Merchant Category', type: 'transaction', description: 'Merchant category code', dtype: 'string', freshness: 'real-time' },
      { id: 'txn_velocity_24h', name: 'Transaction Velocity', type: 'transaction', description: 'Number of transactions in last 24h', dtype: 'int', freshness: 'hourly' },
      { id: 'risk_fraud_score', name: 'Fraud Risk Score', type: 'risk', description: 'ML-generated fraud probability', dtype: 'float', freshness: 'real-time' },
      { id: 'risk_default_probability', name: 'Default Probability', type: 'risk', description: 'Probability of loan default', dtype: 'float', freshness: 'daily' }
    ];
    
    this.filteredFeatures = [...this.features];
    this.currentFilter = 'all';
    
    this.init();
  }

  init() {
    // Bind events
    document.getElementById('search-input').addEventListener('input', (e) => this.search(e.target.value));
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.filter = e.target.dataset.filter;
        this.applyFilter();
      });
    });

    this.render();
  }

  search(query) {
    this.filteredFeatures = this.features.filter(f => 
      f.name.toLowerCase().includes(query.toLowerCase()) || 
      f.description.toLowerCase().includes(query.toLowerCase()) ||
      f.type.toLowerCase().includes(query.toLowerCase())
    );
    this.render();
  }

  applyFilter() {
    if (this.filter === 'all') {
      this.filteredFeatures = [...this.features];
    } else {
      this.filteredFeatures = this.features.filter(f => f.type === this.filter);
    }
    this.render();
  }

  render() {
    const container = document.getElementById('feature-list');
    container.innerHTML = this.filteredFeatures.map(f => `
      <div class="feature-card" onclick="app.showFeature('${f.id}')">
        <div class="feature-header">
          <span class="feature-name">${f.name}</span>
          <span class="feature-type">${f.type}</span>
        </div>
        <div class="feature-description">${f.description}</div>
        <div style="margin-top: 8px; font-size: 0.75rem; color: #64748b;">
          <span>Type: ${f.dtype}</span> • <span>Freshness: ${f.freshness}</span>
        </div>
      </div>
    `).join('');
  }

  showFeature(id) {
    const feature = this.features.find(f => f.id === id);
    const modal = document.getElementById('modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    title.textContent = feature.name;
    body.innerHTML = `
      <p><strong>Description:</strong> ${feature.description}</p>
      <p><strong>Data Type:</strong> ${feature.dtype}</p>
      <p><strong>Category:</strong> ${feature.type}</p>
      <p><strong>Freshness:</strong> ${feature.freshness}</p>
      <p><strong>Usage:</strong> Used in fraud detection, credit scoring models</p>
      <div style="margin-top: 16px; padding: 12px; background: #f0fdf4; border-radius: 8px;">
        <strong>Feature Lineage:</strong>
        <ul style="margin-top: 8px; margin-left: 20px;">
          <li>Source: Transaction DB</li>
          <li>Transformation: Aggregation + Normalization</li>
          <li>Serving: Real-time API</li>
        </ul>
      </div>
    `;
    
    modal.classList.remove('hidden');
  }

  closeModal() {
    document.getElementById('modal').classList.add('hidden');
  }
}

// Global app instance
let app;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  app = new FeatureStore();
});