"""
Merkle Tree for transaction integrity (Lightweight)
"""

import hashlib
from typing import List, Optional


def hash_leaf(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def hash_pair(a: str, b: str) -> str:
    return hashlib.sha256((a + b).encode()).hexdigest()


def build_merkle_tree(tx_hashes: List[str]) -> tuple[Optional[str], List[List[str]]]:
    if not tx_hashes:
        return None, []

    tree: List[List[str]] = [tx_hashes[:]]
    level = tx_hashes[:]

    while len(level) > 1:
        nxt: List[str] = []

        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(hash_pair(left, right))

        tree.append(nxt)
        level = nxt

    return level[0], tree


def verify_merkle_proof(
    tx_hash: str,
    proof: List[str],
    root: str,
    is_left: List[bool]
) -> bool:

    val = tx_hash

    for sibling, sibling_on_left in zip(proof, is_left):
        if sibling_on_left:
            val = hash_pair(sibling, val)
        else:
            val = hash_pair(val, sibling)

    return val == root


def demo():
    transactions = [
        "tx_a",
        "tx_b",
        "tx_c",
        "tx_d",
        "Alice->Bob:50",
        "Bob->Charlie:30",
        "Charlie->Dave:20",
        "Dave->Alice:10"
    ]

    # Hash leaves before building Merkle tree
    leaf_hashes = [hash_leaf(tx) for tx in transactions]

    root, tree = build_merkle_tree(leaf_hashes)

    print("=== Merkle Tree Demo (Finance Tx Integrity) ===")
    print(f"Transactions: {len(transactions)}")
    print(f"Root hash: {root}")

    for i, level in enumerate(tree):
        print(f"  Level {i}: {level}")

    # Verify a proof
    idx = 4

    tx = transactions[idx]
    tx_hash = hash_leaf(tx)

    proof = []
    is_left = []

    pos = idx

    for level in tree[:-1]:

        if pos % 2 == 0:
            sibling_idx = pos + 1

            if sibling_idx >= len(level):
                sibling_idx = pos

            proof.append(level[sibling_idx])
            is_left.append(False)

        else:
            sibling_idx = pos - 1
            proof.append(level[sibling_idx])
            is_left.append(True)

        pos //= 2

    ok = verify_merkle_proof(tx_hash, proof, root, is_left)

    print(f"Proof verification for '{tx}': {ok}")

    # Tamper test
    tampered = transactions[:]
    tampered[0] = "Alice->Bob:999"

    tampered_hashes = [hash_leaf(tx) for tx in tampered]
    root2, _ = build_merkle_tree(tampered_hashes)

    print(f"Root after tamper differs: {root != root2}")
    print("Merkle tree demo complete.")


if __name__ == "__main__":
    demo()