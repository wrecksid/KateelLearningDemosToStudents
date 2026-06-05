# SYNAPSE — Semantic Word Game

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `🤖 Browser-AI-Demos/Browser-AI-Product-Demos/semantic-game/`

A **Wordle-style semantic guessing game** powered by sentence embeddings running in the browser. Players guess a secret daily word; the model scores each guess by its semantic distance to the target — teaching players to think in meaning-space rather than letter-space.

---

## What This Demo Does

| Feature | Detail |
|---------|--------|
| Model | **mixedbread-ai/mxbai-embed-xsmall-v1** — compact, fast embedding model (~40 MB) |
| Game mechanic | Guess the secret word; each guess is scored 0–100% by cosine similarity to the target embedding |
| Daily rotation | Target word changes each day — derived from a seeded word list using `new Date()` day-of-year index |
| Gauge | Animated 0–100% similarity gauge that fills toward the target with each guess |
| Hint system | Visual feedback: red (<30%), amber (30–70%), green (>70%), gold border at 95%+ |
| Leaderboard | In-session guess history with scores listed in order |
| Status bar | Purple diagnostic panel shows model load progress and WebGPU status |

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Complete single-file game — HTML + CSS + JavaScript |

---

## How to Run

```bash
cd "🤖 Browser-AI-Demos/Browser-AI-Product-Demos"
python -m http.server 8080
# Open http://localhost:8080/semantic-game/
```

Requires a **WebGPU-capable browser** (Chrome 113+, Edge 113+). The embedding model downloads ~40 MB on first run and caches in the browser.

---

## Architecture Notes

```
Secret word ──► feature-extraction pipeline ──► target_embedding (cached)

Player types a guess
          │
          ▼
   feature-extraction pipeline
   (mxbai-embed-xsmall-v1)
          │
          ▼
   cosine_similarity(guess_embedding, target_embedding)
          │
          ▼
   Score 0–100% ──► update gauge + history list
```

The daily word is selected deterministically: `wordList[dayOfYear % wordList.length]`, so all players worldwide see the same target word on the same day.

---

## Educational Value

This game demonstrates:
- That word meaning can be **represented as a vector** in high-dimensional space
- That semantically related words (e.g. "ocean" and "sea") have **high cosine similarity**
- That **approximate guesses** can be meaningfully ranked by similarity — not just exact matches

---

## How This Connects to Other Demos

- [`6-semantic-search`](../6-semantic-search/) — same embedding model, same cosine similarity scoring
- [`1-local-chat-advisor`](../1-local-chat-advisor/) — generative complement to this embedding-based demo

---

## Student Extensions

1. Add a **themed word set** (finance terms, medical vocabulary, country names) and observe how guessing strategy changes.
2. Implement a **Give up / Reveal** button that shows the target word and its closest semantic neighbours.
3. Add a **2D visualisation** using PCA: plot all guesses and the target in embedding space as the player guesses.
4. Allow **multiplayer** via a shared URL parameter that encodes the target word index — compare scores with classmates.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
