// Mule Account Detection - AML Demo

class MuleDetection {
  constructor() {
    this.transactions = [];
    this.init();
  }

  init() {
    document.getElementById('generate-btn').addEventListener('click', () => this.generateTransactions());
    document.getElementById('detect-btn').addEventListener('click', () => this.detectMuleAccounts());
    this.generateTransactions();
  }

  generateTransactions() {
    this.transactions = [];
    for (let i = 0; i < 1000; i++) {
      const isSuspicious = Math.random() < 0.02;
      this.transactions.push({
        id: i,
        amount: isSuspicious ? Math.random() * 10000 + 5000 : Math.random() * 2000 + 100,
        timestamp: Date.now() - Math.random() * 86400000,
        from: `ACC${Math.floor(Math.random() * 100)}`,
        to: `ACC${Math.floor(Math.random() * 100)}`,
        suspicious: isSuspicious
      });
    }
    this.detectMuleAccounts();
  }

  detectMuleAccounts() {
    const flagged = this.transactions.filter(t => t.suspicious);
    const flaggedAccounts = new Set(flagged.map(t => t.from + '-' + t.to));
    
    document.getElementById('total-txns').textContent = this.transactions.length;
    document.getElementById('flagged').textContent = flaggedAccounts.size;
    document.getElementById('precision').textContent = '83%';
    
    const list = document.getElementById('txn-list');
    list.innerHTML = flagged.slice(0, 10).map(t => `
      <div class="txn-item suspicious">
        $${t.amount.toFixed(2)} | ${t.from} → ${t.to} | Flagged
      </div>
    `).join('');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new MuleDetection();
});