"""
Day 30 — Searching by words, or by meaning?
===========================================

The handbook's cancellation policy is titled "Reservation Withdrawal", and
never uses the word "cancel". So what happens when a guest asks:

    "How do I cancel my booking?"

This compares KEYWORD search (matching words) with EMBEDDING search
(matching meaning), on the handbook cut by headings.

    python search_demo.py
    python search_demo.py "Is the tap water safe to drink?"

Keyword search needs no key. Embedding search needs an embedding model:
  PROVIDER = "openai"  → needs OPENAI_API_KEY in .env
  PROVIDER = "ollama"  → free: run  ollama pull nomic-embed-text  first
"""

import math
import re
import sys

from dotenv import load_dotenv
from openai import OpenAI

from chunk_explorer import DEFAULT_FILE, by_headings

load_dotenv()

PROVIDER = "openai"          # "openai" or "ollama"

EMBEDDING_MODEL = ("nomic-embed-text" if PROVIDER == "ollama"
                   else "text-embedding-3-small")

COMMON_WORDS = {"how", "do", "i", "my", "the", "a", "an", "is", "to", "of",
                "can", "what", "it", "in", "for", "and", "are", "you"}


def title_of(chunk: str) -> str:
    first_line = chunk.strip().splitlines()[0]
    return first_line.strip("# ").strip()


# ---------------------------------------------------------------------------
# Keyword search: count how many of the question's words appear
# ---------------------------------------------------------------------------

def keyword_search(question, chunks, top=3):
    words = set(re.findall(r"[a-z]+", question.lower())) - COMMON_WORDS
    scored = []
    for chunk in chunks:
        text = chunk.lower()
        score = sum(text.count(word) for word in words)
        scored.append((score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return words, scored[:top]


# ---------------------------------------------------------------------------
# Embedding search: turn text into numbers, and compare the numbers
# ---------------------------------------------------------------------------

def embed(texts):
    # The connection is made only here, so keyword search works with no key.
    if PROVIDER == "ollama":
        client = OpenAI(base_url="http://localhost:11434/v1",
                        api_key="ollama")
    else:
        client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def similarity(a, b):
    """Cosine similarity: 1.0 means the same direction — the same meaning."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) *
                  math.sqrt(sum(y * y for y in b)))


def embedding_search(question, chunks, top=3):
    vectors = embed(chunks + [question])
    question_vector = vectors[-1]
    scored = [(similarity(question_vector, v), c)
              for v, c in zip(vectors[:-1], chunks)]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return len(question_vector), scored[:top]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do I cancel my booking?"
    chunks = by_headings(DEFAULT_FILE.read_text(encoding="utf-8"))
    print(f"\nQUESTION: {question}")
    print(f"Searching {len(chunks)} chunks (cut by headings)\n")

    words, results = keyword_search(question, chunks)
    print(f"KEYWORD SEARCH — looking for the words: {sorted(words)}")
    for score, chunk in results:
        print(f"   {score:>3} matches   {title_of(chunk)}")

    print(f"\nEMBEDDING SEARCH — model: {EMBEDDING_MODEL}")
    try:
        size, results = embedding_search(question, chunks)
        print(f"   (each text became a list of {size} numbers)")
        for score, chunk in results:
            print(f"   {score:.3f} similar   {title_of(chunk)}")
    except Exception as error:
        print(f"   Could not run: {type(error).__name__}. Check the key in "
              f".env, or that Ollama is running.")
