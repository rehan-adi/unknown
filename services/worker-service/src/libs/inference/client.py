import logging
from typing import List

import httpx

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    logger.info(f"Generating embeddings for {len(texts)} chunks...")
    url = f"{ENV_CONFIG.INFERENCE_API_URL}/v1/embeddings"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json={"input": texts, "model": "bge-m3"}, timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return [item["embedding"] for item in data["data"]]
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {str(e)}")
        raise e
