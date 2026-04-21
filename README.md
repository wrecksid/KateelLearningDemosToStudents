File unchanged since last read. The content from the earlier read_file result in this conversation is still current — refer to that instead of re-reading.
- `TechUseCaseDemos\\Forecast\\tsdemo001`
## Blockchain Demos
New lightweight blockchain finance demos added under `TechUseCaseDemos/Blockchain/`:
- `blockchain_finance_demo.py` — basic ledger with PoW mining, balances, chain validation
- `blockchain_smart_contract_escrow.py` — 3-party escrow (create/release/refund) with tamper-evident state
- `blockchain_merkle_tree.py` — Merkle tree construction and inclusion proof verification
- `blockchain_consensus_pow.py` — simplified PoW vs PoS comparison
- `blockchain_payment_channel.py` — payment channel: open → off-chain transfers → settle

## Notes on Demo Compatibility
- Some older demos (Classification/demo001, Clustering/demo001, PatternMining/demo003/fulldemo) require specific dataset schemas not matching the provided synthetic data generators. These demos are provided as educational templates but may need dataset adjustments to run.
- Most demos in TechUseCaseDemos and working DomainUseCaseDemos run correctly with their synthetic data generators.
