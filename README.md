# Day 30 — Giving an Agent Your Own Documents

Today is about understanding the two ideas under every knowledge system —
**chunking** and **embeddings** — before building the full pipeline
tomorrow.

| File | What it does |
|---|---|
| `sample_docs/guesthouse_handbook.md` | A realistic handbook to practise on: headings, a price table, a numbered procedure |
| `chunk_explorer.py` | Cuts a document four ways, and checks whether the table and the procedure stay whole |
| `search_demo.py` | Keyword search vs embedding search, on a question whose answer uses different words |
| `golden_set.md` | A template for your ten test questions |
| `developer-tools/` | Five short guides |

## Setup

    python -m venv .venv
    .venv\Scripts\activate            (Windows)
    source .venv/bin/activate         (Mac or Linux)
    pip install -r requirements.txt

`chunk_explorer.py` and the keyword half of `search_demo.py` need **no key**.
The embedding half needs an OpenAI key in `.env` — or set
`PROVIDER = "ollama"` and run `ollama pull nomic-embed-text`.

## Run it

    python chunk_explorer.py
    python chunk_explorer.py --show characters 9
    python chunk_explorer.py --file path/to/your_document.md

    python search_demo.py
    python search_demo.py "Is the tap water safe to drink?"

## The three ideas to take away

**1. LangChain's default `chunk_size` counts characters, not tokens.**
`chunk_size=512` gives chunks of about 127 tokens. Use
`from_tiktoken_encoder`, or a token-counting `length_function`.

**2. Never split a table or a numbered procedure.** The explorer shows which
strategies do.

**3. Keyword search matches words; embedding search matches meaning.** The
handbook's cancellation policy never says "cancel" — so keyword search
confidently picks the wrong section.
