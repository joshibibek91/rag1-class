# 4. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| "ESTIMATED tokens" | tiktoken couldn't download its token list | Connect to the internet once and run again |
| Embedding search: "Could not run" | No key, or Ollama not running | Add the key to `.env`, or start Ollama |
| `ModuleNotFoundError: langchain_text_splitters` | Packages not installed | `pip install -r requirements.txt` |
| Your PDF won't load | The explorer reads text files | Convert it to text or Markdown first — Day 31 covers PDFs |
| `headings` makes one giant chunk | Your document has no `#` headings | Use `tokens`, or add headings |
