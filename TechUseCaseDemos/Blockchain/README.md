# Blockchain Finance Demos

This directory contains lightweight, educational demos illustrating blockchain concepts applied to finance.

## Demos

- `blockchain_finance_demo.py` — Simple ledger with transactions, balances, proof-of-work mining, and chain validation.
- `blockchain_smart_contract_escrow.py` — Smart-contract-style escrow (create, release, refund) with tamper-evident state.
- `blockchain_merkle_tree.py` — Merkle tree construction and inclusion proof verification for transaction integrity.
- `blockchain_consensus_pow.py` — Comparison of Proof-of-Work and Proof-of-Stake (simplified consensus mechanics).
- `blockchain_payment_channel.py` — Payment channel pattern: open channel, multiple off-chain transfers, settle on-chain.

## Usage

Each demo is self-contained and runs with the standard Python library (no external dependencies):

```bash
python3 TechUseCaseDemos/Blockchain/blockchain_finance_demo.py
python3 TechUseCaseDemos/Blockchain/blockchain_smart_contract_escrow.py
python3 TechUseCaseDemos/Blockchain/blockchain_merkle_tree.py
python3 TechUseCaseDemos/Blockchain/blockchain_consensus_pow.py
python3 TechUseCaseDemos/Blockchain/blockchain_payment_channel.py
```

## Learning Goals

- Basic blockchain data structures (blocks, chains, hashes)
- Proof-of-Work mining and chain validation
- Simplified Proof-of-Stake validator selection
- Merkle trees for transaction integrity
- Off-chain scaling pattern: payment channels / simple smart contracts
- Tamper detection and immutability principles
