# 6 — Semantic Search

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/6-semantic-search/`

A **vector-based semantic search engine** that runs entirely in the browser. Type a query and it returns the most relevant documents by cosine similarity over sentence embeddings — no keyword matching, no external search API, no server.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **all-MiniLM-L6-v2** (feature-extraction pipeline) — ~90 MB sentence embedding model |
| Similarity | Cosine similarity: `sim(A,B) = (A · B) / (‖A‖ · ‖B‖)` |
| Documents | 10 pre-loaded sample documents across finance, technology, and science topics |
| Add-your-own | Text area to add custom documents — they are embedded and included in future searches |
| Results | Ranked list of documents with similarity score (0–100%) shown for each |
| Status bar | Orange/amber progress gradient during model download |

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete single-file demo — HTML + CSS + JavaScript |

---

## How to Run

```bash
cd "🤖 Browser-AI-Demos/Browser-AI-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/6-semantic-search/
```

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). all-MiniLM-L6-v2 downloads ~90 MB on first run and caches in the browser.

---

## Architecture Notes

```
All documents embedded at startup ──► embedding cache (Float32Array[])
              │
       User enters query
              │
              ▼
   feature-extraction pipeline
   (all-MiniLM-L6-v2)
              │
              ▼
   query embedding (384-dim vector)
              │
              ▼
   cosine_similarity(query_emb, doc_emb[i]) for each doc
              │
              ▼
   Sort descending by score ──► render ranked results
```

Documents added via the "Add document" field are embedded on the fly and appended to the cache — no page reload needed.

---

## Cosine Similarity Formula

```
similarity = (Σ Aᵢ × Bᵢ) / (√Σ Aᵢ² × √Σ Bᵢ²)
```

Score = 1.0 → identical meaning; Score = 0.0 → unrelated; Score < 0 → opposite meanings.

---

## How This Connects to Other Demos

- [`semantic-game`](../semantic-game/) — same embedding model used in a word-guessing game
- [`5-entity-tagger`](../5-entity-tagger/) — extract entities first, then search over them semantically

---

## Student Extensions

1. Replace the pre-loaded documents with product descriptions from a CSV — build a product recommendation engine.
2. Add **bi-encoder re-ranking** using a cross-encoder model on the top-5 results.
3. Implement **approximate nearest neighbour** (e.g. HNSW) for larger document sets.
4. Visualise the embedding space with **PCA / UMAP** — plot query and documents in 2D to show clustering.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
