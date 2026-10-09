import logging
from typing import List

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def fetch_sitemap_urls(sitemap_url: str) -> List[str]:
    logger.info(f"Crawling sitemap: {sitemap_url}")
    urls = []
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(sitemap_url, timeout=30.0)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            loc_tags = soup.find_all("loc")

            for tag in loc_tags:
                if tag.text:
                    urls.append(tag.text.strip())

        return urls
    except Exception as e:
        logger.error(f"Failed to crawl sitemap: {str(e)}")
        raise e
