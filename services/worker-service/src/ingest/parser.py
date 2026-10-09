import logging

from unstructured.partition.html import partition_html

logger = logging.getLogger(__name__)


def parse_html_to_markdown(html_content: str) -> str:
    try:
        elements = partition_html(text=html_content)
        return "\n\n".join([str(element) for element in elements])
    except Exception as e:
        logger.error(f"Failed to parse HTML with unstructured: {str(e)}")
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator="\n", strip=True)
