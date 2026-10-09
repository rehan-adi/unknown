# Worker Service

This service handles the heavy lifting of the RAG pipeline:

1. Crawling (Web, Sitemap, GitHub)
2. Parsing (HTML to Markdown via `unstructured`)
3. Chunking (Heading-aware)
4. Embedding (via Inference Service)
5. Upserting (to Qdrant and Postgres database)

## Development

```bash
# Install dependencies
uv lock
uv sync

# Format code
ruff format .
```
