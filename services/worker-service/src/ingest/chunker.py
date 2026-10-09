from typing import Dict, List

from unstructured.chunking.title import chunk_by_title
from unstructured.partition.md import partition_md


def chunk_markdown(text: str) -> List[Dict]:
    """
    Semantic Chunking:
    Instead of cutting text at a random 1000 character limit (which cuts sentences in half),
    this uses Machine Learning to logically group paragraphs under their section titles.
    """
    # 1. Parse the Markdown into structural elements (Titles, Paragraphs, Lists)
    elements = partition_md(text=text)

    # 2. Chunk elements semantically by Title/Section boundaries
    chunks = chunk_by_title(
        elements,
        max_characters=1500,
        new_after_n_chars=1200,
        combine_text_under_n_chars=400,
    )

    result = []
    for chunk in chunks:
        result.append({"heading": "Semantic Chunk", "content": str(chunk)})

    return result
