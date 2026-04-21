"""
Lightweight Blockchain-based Finance Demo
=========================================
A simple demonstration of blockchain concepts for finance:
- Transaction ledger simulation
- Proof-of-Work mining
- Transaction validation
- Simple smart contract (escrow)
"""

import hashlib
import json
import time
from typing import List, Dict, Optional


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }

    def hash(self) -> str:
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()

    def __repr__(self) -> str:
        return f"Tx({self.sender[:6]}->{self.receiver[:6]}:{self.amount})"


class Block:
    def __init__(self, index: int, prev_hash: str, transactions: List[Transaction], nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.nonce = nonce
        self.prev_hash = prev_hash

    def compute_hash(self) -> str:
        block_str = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce,
            "prev_hash": self.prev_hash,
        }, sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"Block#{self.index}"


class SimpleBlockchain:
    DIFFICULTY = "00"  # Proof-of-Work target prefix

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_txs: List[Transaction] = []
        self.balances: Dict[str, float] = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", [])
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> str:
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith(self.DIFFICULTY):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_transaction(self, sender: str, receiver: str, amount: float) -> bool:
        if self.balances.get(sender, 0) < amount:
            return False
        tx = Transaction(sender, receiver, amount)
        self.pending_txs.append(tx)
        return True

    def mine_pending(self) -> Optional[Block]:
        if not self.pending_txs:
            return None
        new_block = Block(
            index=len(self.chain),
            prev_hash=self.last_block.compute_hash(),
            transactions=self.pending_txs[:],
        )
        new_block.hash = self.proof_of_work(new_block)
        # Update balances
        for tx in self.pending_txs:
            self.balances[tx.sender] = self.balances.get(tx.sender, 100.0) - tx.amount
            self.balances[tx.receiver] = self.balances.get(tx.receiver, 0.0) + tx.amount
        self.chain.append(new_block)
        self.pending_txs.clear()
        return new_block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if cur.prev_hash != prev.compute_hash():
                return False
            if not cur.compute_hash().startswith(self.DIFFICULTY):
                return False
        return True

    def print_chain(self):
        for blk in self.chain:
            print(f"  {blk} hash={blk.compute_hash()[:12]}...")
            for t in blk.transactions:
                print(f"    {t}")


def demo():
    chain = SimpleBlockchain()
    # Fund accounts
    chain.balances.update({"Alice": 100.0, "Bob": 50.0, "Charlie": 25.0})
    print("=== Simple Blockchain Finance Demo ===")
    print(f"Genesis: {chain.last_block}")
    print()

    # Transactions
    chain.add_transaction("Alice", "Bob", 10.0)
    chain.add_transaction("Bob", "Charlie", 5.0)
    chain.add_transaction("Alice", "Charlie", 15.0)
    print("Pending transactions:", chain.pending_txs)

    mined = chain.mine_pending()
    print(f"Mined: {mined}")
    chain.print_chain()
    print(f"Balances: {chain.balances}")

    # Invalid attempt test
    ok = chain.add_transaction("Charlie", "Alice", 1000.0)  # insufficient
    print(f"Invalid tx (insufficient funds): {ok}")

    # Tamper test
    if len(chain.chain) > 1:
        chain.chain[1].transactions[0].amount = 999.0
        print(f"Chain valid after tamper: {chain.is_valid()}")

    print("\nBlockchain finance demo complete.")


if __name__ == "__main__":
    demo()
