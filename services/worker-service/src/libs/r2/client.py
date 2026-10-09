import asyncio
import logging

import boto3

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{ENV_CONFIG.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=ENV_CONFIG.R2_ACCESS_KEY_ID,
        aws_secret_access_key=ENV_CONFIG.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


async def download_file_from_r2(object_key: str) -> bytes:
    logger.info(f"Downloading {object_key} from R2...")
    client = get_r2_client()

    def _download():
        response = client.get_object(Bucket=ENV_CONFIG.R2_BUCKET_NAME, Key=object_key)
        return response["Body"].read()

    # Run blocking boto3 call in a background thread to prevent freezing the asyncio loop
    return await asyncio.to_thread(_download)
