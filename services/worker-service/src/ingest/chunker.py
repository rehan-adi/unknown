import re
from typing import Dict, List


def chunk_markdown(text: str, max_chunk_size: int = 1000) -> List[Dict]:
    lines = text.split("\n")
    chunks = []
    current_heading = ""
    current_chunk = ""
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block

        if not in_code_block and re.match(r"^#{1,6}\s", line):
            if current_chunk.strip():
                chunks.append({"heading": current_heading, "content": current_chunk.strip()})
            current_heading = line.strip()
            current_chunk = ""
        else:
            current_chunk += line + "\n"
            if len(current_chunk) > max_chunk_size and not in_code_block:
                chunks.append({"heading": current_heading, "content": current_chunk.strip()})
                current_chunk = ""

    if current_chunk.strip():
        chunks.append({"heading": current_heading, "content": current_chunk.strip()})

    return chunks
