import logging
import uuid

import asyncpg

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


async def get_db_connection():
    return await asyncpg.connect(ENV_CONFIG.DATABASE_URL)


async def update_job_status(job_id: str, status: str, progress: int = 0, error_message: str = None):
    try:
        conn = await get_db_connection()
        await conn.execute(
            """
            UPDATE ingestion_jobs 
            SET status = $1, progress = $2, error_message = $3, updated_at = NOW()
            WHERE id = $4
            """,
            status,
            progress,
            error_message,
            job_id,
        )
        await conn.close()
    except Exception as e:
        logger.error(f"Failed to update job status: {e}")


async def check_document_hash(project_id: str, url: str, content_hash: str) -> bool:
    try:
        conn = await get_db_connection()
        record = await conn.fetchrow(
            """
            SELECT id FROM documents 
            WHERE url = $1 AND content_hash = $2
            """,
            url,
            content_hash,
        )
        await conn.close()
        return bool(record)
    except Exception as e:
        logger.error(f"Failed to check document hash: {e}")
        return False


async def save_document_metadata(
    source_id: str, url: str, title: str, content_hash: str, raw_content: str, chunks_metadata: list
):
    try:
        conn = await get_db_connection()

        doc_id = str(uuid.uuid4())

        existing_doc = await conn.fetchrow(
            "SELECT id FROM documents WHERE source_id = $1 AND url = $2", source_id, url
        )

        if existing_doc:
            doc_id = existing_doc["id"]
            await conn.execute(
                """
                UPDATE documents 
                SET title = $1, content_hash = $2, content = $3, updated_at = NOW()
                WHERE id = $4
                """,
                title,
                content_hash,
                raw_content,
                doc_id,
            )
            await conn.execute("DELETE FROM chunks WHERE document_id = $1", doc_id)
        else:
            await conn.execute(
                """
                INSERT INTO documents (
                    id, source_id, url, title, content_hash, content, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
                """,
                doc_id,
                source_id,
                url,
                title,
                content_hash,
                raw_content,
            )

        for index, chunk in enumerate(chunks_metadata):
            await conn.execute(
                """
                INSERT INTO chunks (
                    id, document_id, content, heading, chunk_index, tokens, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, NOW())
                """,
                str(uuid.uuid4()),
                doc_id,
                chunk["content"],
                chunk.get("heading"),
                index,
                0,
            )

        await conn.close()
    except Exception as e:
        logger.error(f"Failed to save document metadata: {e}")
        raise e
