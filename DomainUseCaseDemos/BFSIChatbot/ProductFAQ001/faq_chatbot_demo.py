from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_sections(markdown_path: Path):
    text = markdown_path.read_text(encoding="utf-8")
    chunks = [chunk.strip() for chunk in re.split(r"(?=^## )", text, flags=re.MULTILINE) if chunk.strip()]
    titles = []
    bodies = []
    for chunk in chunks:
        lines = chunk.splitlines()
        titles.append(lines[0].replace("## ", "").strip())
        bodies.append(" ".join(lines[1:]).strip())
    return titles, bodies


def answer_query(query: str, titles, bodies):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(bodies + [query])
    similarities = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    best_idx = similarities.argmax()
    return titles[best_idx], bodies[best_idx], similarities[best_idx]


def main():
    kb_path = Path("knowledge_base.md")
    if not kb_path.exists():
        raise FileNotFoundError("knowledge_base.md not found.")

    titles, bodies = load_sections(kb_path)
    sample_queries = [
        "How do I dispute a failed UPI payment?",
        "What documents are needed for an insurance claim?",
        "When is the credit card fee waived?",
    ]

    for query in sample_queries:
        title, body, score = answer_query(query, titles, bodies)
        print(f"\nQuery: {query}")
        print(f"Best Match: {title} (score={score:.3f})")
        print(body)


if __name__ == "__main__":
    main()
