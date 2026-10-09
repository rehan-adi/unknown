import logging
import uuid
from typing import Dict, List

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


async def save_to_qdrant(
    collection_name: str,
    chunks: List[Dict],
    embeddings: List[List[float]],
    source_id: str,
    url: str,
):
    client = AsyncQdrantClient(url=ENV_CONFIG.QDRANT_URL)

    collections = await client.get_collections()
    if not any(c.name == collection_name for c in collections.collections):
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE),
        )

    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "source_id": source_id,
                    "url": url,
                    "chunk_index": i,
                    "heading": chunk.get("heading", ""),
                    "content": chunk.get("content", ""),
                },
            )
        )

    batch_size = 100
    for i in range(0, len(points), batch_size):
        await client.upsert(collection_name=collection_name, points=points[i : i + batch_size])

    logger.info(f"Successfully saved {len(points)} vectors to Qdrant.")


async def delete_old_vectors(collection_name: str, url: str):
    client = AsyncQdrantClient(url=ENV_CONFIG.QDRANT_URL)
    try:
        collections = await client.get_collections()
        if not any(c.name == collection_name for c in collections.collections):
            return

        await client.delete(
            collection_name=collection_name,
            points_selector=Filter(must=[FieldCondition(key="url", match=MatchValue(value=url))]),
        )
        logger.info(f"Deleted old vectors for URL: {url}")
    except Exception as e:
        logger.warning(f"Failed to delete old vectors: {str(e)}")
