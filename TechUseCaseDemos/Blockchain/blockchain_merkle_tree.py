"""
Merkle Tree for transaction integrity (Lightweight)
"""

import hashlib
from typing import List, Optional


def hash_pair(a: str, b: str) -> str:
    return hashlib.sha256((a + b).encode()).hexdigest()


def build_merkle_tree(tx_hashes: List[str]) -> tuple[Optional[str], List[List[str]]]:
    if not tx_hashes:
        return None, []
    tree: List[List[str]] = [tx_hashes[:]]
    level = tx_hashes
    while len(level) > 1:
        nxt: List[str] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(hash_pair(left, right))
        tree.append(nxt)
        level = nxt
    return level[0], tree


def verify_merkle_proof(tx_hash: str, proof: List[str], root: str, is_left: List[bool]) -> bool:
    val = tx_hash
    for p, left in zip(proof, is_left):
        val = hash_pair(p, val) if left else hash_pair(val, p)
    return val == root


def demo():
    transactions = [
        "tx_a", "tx_b", "tx_c", "tx_d",
        "Alice->Bob:50", "Bob->Charlie:30", "Charlie->Dave:20", "Dave->Alice:10"
    ]
    root, tree = build_merkle_tree(transactions)
    print("=== Merkle Tree Demo (Finance Tx Integrity) ===")
    print(f"Transactions: {len(transactions)}")
    print(f"Root hash: {root}")
    for i, level in enumerate(tree):
        print(f"  Level {i}: {level}")

    # Verify a proof
    idx = 4
    tx = transactions[idx]
    proof = []
    is_left = []
    pos = idx
    for level in tree[:-1]:
        if pos + 1 < len(level):
            proof.append(level[pos + 1])
            is_left.append(pos % 2 == 0)
        else:
            proof.append(level[pos])  # duplicate for odd count
            is_left.append(True)
        pos //= 2
    ok = verify_merkle_proof(tx, proof, root, is_left)
    print(f"Proof verification for '{tx}': {ok}")

    # Tamper test
    tampered = transactions[:]
    tampered[0] = "Alice->Bob:999"
    root2, _ = build_merkle_tree(tampered)
    print(f"Root after tamper differs: {root != root2}")
    print("Merkle tree demo complete.")


if __name__ == "__main__":
    demo()
