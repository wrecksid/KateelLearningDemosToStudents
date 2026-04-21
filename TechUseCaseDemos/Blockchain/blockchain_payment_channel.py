"""
Payment Channel (Off-chain) Demo - lightweight blockchain finance pattern
Simulates opening/settling a payment channel between two parties.
"""

import hashlib
import json
import time
from typing import Optional, Dict


def hash_data(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class PaymentChannel:
    def __init__(self, payer: str, payee: str, deposit: float):
        self.payer = payer
        self.payee = payee
        self.deposit = deposit
        self.balance_payer = deposit
        self.balance_payee = 0.0
        self.nonce = 0
        self.open = True
        self.settlement_tx: Optional[dict] = None

    def transfer(self, from_party: str, to_party: str, amount: float) -> bool:
        if not self.open:
            return False
        if from_party == self.payer and self.balance_payer < amount:
            return False
        if from_party == self.payer:
            self.balance_payer -= amount
            self.balance_payee += amount
        else:
            return False  # only payer can pay in this simple model
        self.nonce += 1
        return True

    def close_and_settle(self) -> dict:
        if not self.open:
            raise ValueError("Channel already closed")
        self.open = False
        settlement = {
            "payer": self.payer,
            "payee": self.payee,
            "final_payer_balance": self.balance_payer,
            "final_payee_balance": self.balance_payee,
            "timestamp": time.time(),
            "nonce": self.nonce,
        }
        settlement["tx_hash"] = hash_data(settlement)
        self.settlement_tx = settlement
        return settlement

    def state(self) -> dict:
        return {
            "payer": self.payer,
            "payee": self.payee,
            "deposit": self.deposit,
            "balance_payer": self.balance_payer,
            "balance_payee": self.balance_payee,
            "open": self.open,
            "nonce": self.nonce,
        }


def demo():
    channel = PaymentChannel("Alice", "Bob", 100.0)
    print("=== Payment Channel Demo ===")
    print(f"Opened: {channel.state()}")
    channel.transfer("Alice", "Bob", 20.0)
    print(f"After Alice pays Bob 20: {channel.state()}")
    channel.transfer("Alice", "Bob", 30.0)
    print(f"After Alice pays Bob 30: {channel.state()}")
    settlement = channel.close_and_settle()
    print(f"Settled: {settlement}")
    print("Payment channel demo complete.")


if __name__ == "__main__":
    demo()
