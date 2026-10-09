# Unknown Worker Service

The Worker Service is the background service responsible for processing ingestion jobs autonomously. It consumes jobs from RabbitMQ, crawls websites, parses PDFs via Cloudflare R2, extracts and chunks text, generates vector embeddings, and stores the final data in Qdrant and PostgreSQL.

## Core Responsibilities
- **RabbitMQ Consumer**: Listens to `ingestion_queue` for incoming tasks.
- **Sitemap & Web Crawling**: Recursively fans out sitemaps and downloads raw HTML with exponential backoff and polite rate-limiting.
- **PDF Parsing**: Connects to Cloudflare R2 (`boto3`) and extracts clean text using `unstructured[pdf]` ML models.
- **Vector Pipeline**: Generates `bge-m3` embeddings (via Inference Service) and upserts them into Qdrant.
- **Database Tracking**: Updates Postgres job statuses and tracks delta-hashes via Raw SQL (`asyncpg`).

## Running Locally

1. Create a `.env` file based on `.env.example`.
2. Ensure you have `uv` installed.
3. Run the worker from the root of the project:
```bash
bun run start:worker-service
```

## Environment Variables
The worker uses `pydantic-settings` to enforce strict environment configuration. See `.env.example` for all required Database, RabbitMQ, R2, and Sentry variables.
