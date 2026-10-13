# 2. Chunking reference

## The strategies in `chunk_explorer.py`

| Name | What it does |
|---|---|
| `fixed` | Cuts every 2,048 characters, wherever that falls |
| `characters` | LangChain's recursive splitter with its DEFAULT settings — counts characters |
| `tokens` | The same splitter, counting real tokens: about 512 per chunk |
| `headings` | One chunk per section; very long sections are split further |

## The trap — tested

    RecursiveCharacterTextSplitter(chunk_size=512)

gives chunks of at most 512 **characters** — about 127 tokens. To get 512
**tokens**:

    RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=512, chunk_overlap=64)

## What the evidence says (checked September 2026)

| Finding | Source |
|---|---|
| Recursive splitting at 512 tokens: 69% answer accuracy. Semantic chunking: 54%, with fragments averaging 43 tokens | FloTorch benchmark, February 2026, 50 academic papers |
| But semantic chunking had the BEST retrieval recall (91.9%) | Chroma's research |
| Overlap gave no measurable benefit, and raised indexing cost | A January 2026 study |
| Topic-aligned chunking: 87% of clinical answers judged accurate, against 50% for fixed-size | Gomez-Cabello and colleagues, 2025 |

Notice the second row. **Retrieval tests and answer tests measure different
things**, and a method can win one and lose the other. Always ask which a
number measures.

## Two rules that override everything

1. Never split a table.
2. Never split a numbered procedure.
