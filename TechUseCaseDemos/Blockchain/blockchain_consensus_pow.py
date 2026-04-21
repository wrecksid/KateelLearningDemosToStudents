"""
Consensus mechanism demo: Proof-of-Work vs Proof-of-Stake (simplified)
"""

import hashlib
import random
import time


def pow_hash(data: str, nonce: int) -> str:
    return hashlib.sha256(f"{data}{nonce}".encode()).hexdigest()


def proof_of_work(data: str, difficulty: int = 4) -> tuple[int, str]:
    prefix = "0" * difficulty
    nonce = 0
    start = time.time()
    while True:
        h = pow_hash(data, nonce)
        if h.startswith(prefix):
            return nonce, h
        nonce += 1
    return nonce, ""


def proof_of_stake_validators(validators: dict[str, int], seed: int) -> str:
    # weighted random choice by stake
    total = sum(validators.values())
    r = random.Random(seed).randint(1, total)
    acc = 0
    for v, stake in validators.items():
        acc += stake
        if r <= acc:
            return v
    return list(validators.keys())[0]


def demo():
    data = "FinanceTx:Alice->Bob:100"
    print("=== Consensus Mechanisms Demo ===")
    # PoW
    print("\n--- Proof-of-Work ---")
    t = time.time()
    nonce, h = proof_of_work(data, difficulty=4)
    elapsed = time.time() - t
    print(f"Found nonce={nonce}, hash={h[:20]}..., time={elapsed:.3f}s")

    # PoS
    print("\n--- Proof-of-Stake (simplified) ---")
    validators = {"ValidatorA": 40, "ValidatorB": 30, "ValidatorC": 30}
    chosen = proof_of_stake_validators(validators, seed=42)
    print(f"Validators: {validators}")
    print(f"Chosen validator for block: {chosen}")
    print("\nConsensus demo complete.")


if __name__ == "__main__":
    demo()
