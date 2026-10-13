# 1. Setup guide

    pip install -r requirements.txt

## tiktoken needs the internet — once

`tiktoken` counts tokens the way OpenAI's models do. The **first** time it
runs, it downloads its list of tokens from the internet, then keeps a copy.
After that it works offline.

If the download is blocked, `chunk_explorer.py` still works: it says
"ESTIMATED tokens" and counts about 4 characters per token instead. The
comparison still holds — but the sizes are approximate.

## Embeddings

| Setting in `search_demo.py` | What you need |
|---|---|
| `PROVIDER = "openai"` | An OpenAI key in `.env` |
| `PROVIDER = "ollama"` | Ollama running, then `ollama pull nomic-embed-text` |
