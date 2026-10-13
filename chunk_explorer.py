"""
Day 30 — Chunk explorer
=======================

Cuts a document into chunks four different ways, and checks each one:
how many chunks, how big, and whether the price TABLE and the numbered
check-in PROCEDURE each stayed in one piece.

    python chunk_explorer.py                       compare all four
    python chunk_explorer.py --show headings 4     read chunk 4 on its own
    python chunk_explorer.py --file my_notes.md    use your own document

No API key is needed.
"""

import argparse
import re
from pathlib import Path

from langchain_text_splitters import (MarkdownHeaderTextSplitter,
                                      RecursiveCharacterTextSplitter)

DEFAULT_FILE = Path(__file__).parent / "sample_docs" / "guesthouse_handbook.md"
CHUNK_TOKENS = 512
OVERLAP_TOKENS = 64

# ---------------------------------------------------------------------------
# Counting tokens. tiktoken downloads its token list from the internet the
# first time; if that isn't possible, we estimate (about 4 characters each).
# ---------------------------------------------------------------------------
try:
    import tiktoken
    _encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(_encoding.encode(text))
    COUNTING = "real tokens (tiktoken)"
except Exception:
    def count_tokens(text: str) -> int:
        return max(1, len(text) // 4)
    COUNTING = "ESTIMATED tokens (tiktoken unavailable: 4 characters each)"


# ---------------------------------------------------------------------------
# The four ways to cut a document
# ---------------------------------------------------------------------------

def fixed_size(text):
    """Cut every 2,048 characters (about 512 tokens), wherever that falls."""
    size = CHUNK_TOKENS * 4
    return [text[i:i + size] for i in range(0, len(text), size)]


def recursive_characters(text):
    """THE TRAP: LangChain's default counts CHARACTERS, not tokens."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=512,
                                              chunk_overlap=64)
    return splitter.split_text(text)


def recursive_tokens(text):
    """The benchmark default: about 512 TOKENS, split on paragraphs first."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_TOKENS, chunk_overlap=OVERLAP_TOKENS,
        length_function=count_tokens)
    return splitter.split_text(text)


def by_headings(text):
    """Structure-aware: one chunk per section; split only very long ones."""
    sections = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "title"), ("##", "section")],
        strip_headers=False).split_text(text)
    chunks = []
    for section in sections:
        if count_tokens(section.page_content) <= CHUNK_TOKENS:
            chunks.append(section.page_content)
        else:
            chunks.extend(recursive_tokens(section.page_content))
    return chunks


STRATEGIES = {
    "fixed": fixed_size,
    "characters": recursive_characters,
    "tokens": recursive_tokens,
    "headings": by_headings,
}


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------

def find_blocks(text, pattern):
    """Find runs of consecutive lines that match a pattern."""
    blocks, current = [], []
    for line in text.splitlines():
        if re.match(pattern, line.strip()):
            current.append(line.strip())
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def stays_whole(block, chunks):
    """True if at least one chunk contains every line of the block."""
    return any(all(line in chunk for line in block) for chunk in chunks)


def compare(text):
    tables = find_blocks(text, r"^\|")
    procedures = find_blocks(text, r"^\d+\.\s")
    print(f"\nCounting: {COUNTING}")
    print(f"Document: {count_tokens(text)} tokens\n")
    print(f"{'Strategy':12} {'Chunks':>6} {'Average':>8} {'Largest':>8}"
          f"   {'Table whole?':13} {'Procedure whole?'}")
    for name, cut in STRATEGIES.items():
        chunks = cut(text)
        sizes = [count_tokens(c) for c in chunks]
        table_ok = all(stays_whole(t, chunks) for t in tables)
        steps_ok = all(stays_whole(p, chunks) for p in procedures)
        print(f"{name:12} {len(chunks):>6} {sum(sizes) // len(sizes):>8} "
              f"{max(sizes):>8}   {'yes' if table_ok else 'NO — split':13} "
              f"{'yes' if steps_ok else 'NO — split'}")
    print("\nAverage and Largest are in tokens. Read any chunk on its own:\n"
          "  python chunk_explorer.py --show headings 4")


def show(text, strategy, number):
    chunks = STRATEGIES[strategy](text)
    if not 1 <= number <= len(chunks):
        print(f"'{strategy}' made {len(chunks)} chunks. Choose 1 to "
              f"{len(chunks)}.")
        return
    chunk = chunks[number - 1]
    print(f"\n── {strategy}, chunk {number} of {len(chunks)} "
          f"({count_tokens(chunk)} tokens) ──\n")
    print(chunk)
    print("\n── Does it make sense on its own? That is how the model "
          "sees it. ──")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--show", nargs=2, metavar=("STRATEGY", "NUMBER"))
    args = parser.parse_args()
    document = args.file.read_text(encoding="utf-8")
    if args.show:
        show(document, args.show[0], int(args.show[1]))
    else:
        compare(document)
