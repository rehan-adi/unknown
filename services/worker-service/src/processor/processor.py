import io
import json
import logging
import uuid

import aio_pika

from ingest.chunker import chunk_markdown
from ingest.crawler import fetch_url
from ingest.delta import generate_hash
from ingest.parser import parse_html_to_markdown
from ingest.sitemap import fetch_sitemap_urls
from libs.db.client import check_document_hash, save_document_metadata, update_job_status
from libs.inference.client import get_embeddings
from libs.qdrant.client import delete_old_vectors, save_to_qdrant
from libs.r2.client import download_file_from_r2
from libs.rabbitmq.publisher import publish_job

logger = logging.getLogger(__name__)


async def process_job(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process(requeue=True, reject_on_redelivered=True):
        body = json.loads(message.body.decode())
        job_id = body.get("job_id")
        job_type = body.get("job_type", "page")
        source_id = body.get("source_id")
        url = body.get("url")
        project_id = body.get("project_id", "default_project")
        title = body.get("title", "Untitled Document")

        logger.info(f"Received {job_type} job {job_id} for URL {url}")

        try:
            if job_type == "sitemap":
                await update_job_status(job_id, "PARSING", 10)
                urls = await fetch_sitemap_urls(url)
                for child_url in urls:
                    await publish_job(
                        {
                            "job_id": f"job_child_{uuid.uuid4().hex[:8]}",
                            "job_type": "page",
                            "source_id": source_id,
                            "project_id": project_id,
                            "url": child_url,
                            "title": f"Page from {url}",
                        }
                    )
                logger.info(f"Sitemap {url} expanded into {len(urls)} pages. Jobs published.")
                await update_job_status(job_id, "COMPLETED", 100)
                return

            if job_type == "pdf":
                await update_job_status(job_id, "PARSING", 10)
                pdf_bytes = await download_file_from_r2(url)  # url here is the R2 object key

                logger.info(f"Extracting text from PDF {url}...")

                # Lazy import to avoid 5-10 second boot time penalty for normal crawling
                from unstructured.partition.pdf import partition_pdf

                elements = partition_pdf(file=io.BytesIO(pdf_bytes))
                clean_text = "\n\n".join([str(e) for e in elements])

            else:
                # --- NORMAL PAGE PROCESSING ---
                await update_job_status(job_id, "PARSING", 10)
                raw_html = await fetch_url(url)
                clean_text = parse_html_to_markdown(raw_html)

            content_hash = generate_hash(clean_text)
            is_match = await check_document_hash(project_id, url, content_hash)

            if is_match:
                logger.info(f"Hash match for {url}. No changes detected. Skipping.")
                await update_job_status(job_id, "COMPLETED", 100)
                return

            await update_job_status(job_id, "CHUNKING", 30)
            chunks = chunk_markdown(clean_text)
            if not chunks:
                raise ValueError("No text could be extracted for chunking.")

            collection_name = f"project_{project_id}"
            await delete_old_vectors(collection_name, url)

            await update_job_status(job_id, "EMBEDDING", 60)
            texts_to_embed = [c["content"] for c in chunks]
            embeddings = await get_embeddings(texts_to_embed)

            await update_job_status(job_id, "COMPLETED", 90)
            await save_to_qdrant(collection_name, chunks, embeddings, source_id, url)

            chunk_meta = [
                {"heading": c.get("heading", ""), "content": c.get("content", "")} for c in chunks
            ]
            await save_document_metadata(
                source_id, url, title, content_hash, clean_text, chunk_meta
            )

            await update_job_status(job_id, "COMPLETED", 100)
            logger.info(f"Job {job_id} completed successfully.")

        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}")
            await update_job_status(job_id, "FAILED", 0, str(e))
            raise e
