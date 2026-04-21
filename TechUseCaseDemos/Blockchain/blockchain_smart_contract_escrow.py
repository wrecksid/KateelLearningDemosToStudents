"""
Smart Contract Escrow Demo (Blockchain-inspired)
Simulates a 3-party escrow: Buyer -> Escrow -> Seller release.
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EscrowContract:
    buyer: str
    seller: str
    arbiter: str
    amount: float
    state: str = "pending"  # pending, released, refunded
    tx_hash: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    def hash(self):
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()


class EscrowSmartContract:
    def __init__(self):
        self.contracts: dict[str, EscrowContract] = {}

    def create_escrow(self, buyer: str, seller: str, arbiter: str, amount: float) -> str:
        contract = EscrowContract(buyer=buyer, seller=seller, arbiter=arbiter, amount=amount)
        contract.tx_hash = contract.hash()
        self.contracts[contract.tx_hash] = contract
        return contract.tx_hash

    def release(self, tx_hash: str, arbiter_ok: bool = True) -> bool:
        c = self.contracts.get(tx_hash)
        if not c or c.state != "pending":
            return False
        if arbiter_ok:
            c.state = "released"
        else:
            c.state = "refunded"
        return True

    def refund(self, tx_hash: str) -> bool:
        return self.release(tx_hash, arbiter_ok=False)

    def status(self, tx_hash: str) -> Optional[EscrowContract]:
        return self.contracts.get(tx_hash)

    def summary(self) -> dict:
        total = len(self.contracts)
        released = sum(1 for c in self.contracts.values() if c.state == "released")
        refunded = sum(1 for c in self.contracts.values() if c.state == "refunded")
        return {"total": total, "released": released, "refunded": refunded, "pending": total - released - refunded}


def demo():
    esc = EscrowSmartContract()
    print("=== Blockchain Escrow Smart Contract Demo ===")
    # Create an escrow
    tx = esc.create_escrow("Alice", "Bob", "Charlie", 250.0)
    print(f"Created escrow: {tx[:12]}...")
    c = esc.status(tx)
    print(f"  State: {c.state}, Amount: {c.amount}, Buyer: {c.buyer}, Seller: {c.seller}")

    # Release by arbiter
    esc.release(tx, arbiter_ok=True)
    c = esc.status(tx)
    print(f"After release: {c.state}")

    # Another with refund
    tx2 = esc.create_escrow("Dave", "Eve", "Frank", 100.0)
    esc.refund(tx2)
    print(f"Escrow2 state: {esc.status(tx2).state}")

    print(f"Summary: {esc.summary()}")
    print("Escrow demo complete.")


if __name__ == "__main__":
    demo()
