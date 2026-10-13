# 3. Experiments

## 1. Find the trap
    python chunk_explorer.py
Compare `characters` with `tokens`. Same splitter, four times the chunks.

## 2. Read a chunk on its own
    python chunk_explorer.py --show characters 9
Does it say what it is about? Now try `--show headings 5`.

## 3. Search by words, and by meaning
    python search_demo.py
Keyword search picks the wrong section. Does embedding search find
"Reservation Withdrawal"?

## 4. Where keyword search wins
    python search_demo.py "Is the tap water safe to drink?"
When the guest uses the document's own words, keywords work well. Hold that
thought for Day 32.

## 5. Your own document
    python chunk_explorer.py --file my_document.md
Which strategy keeps your tables and procedures whole?
