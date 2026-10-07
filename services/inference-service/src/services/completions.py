import json
from collections.abc import AsyncGenerator

import httpx

from ..config.config import ENV_CONFIG
from ..types.completion import CompletionRequest


async def stream_chat(request: CompletionRequest) -> AsyncGenerator[str]:
    url = f"{ENV_CONFIG.OLLAMA_URL}/api/chat"
    payload = {
        "model": request.model,
        "messages": [{"role": m.role, "content": m.content} for m in request.messages],
        "stream": True,
        "options": {"temperature": request.temperature},
    }

    async with (
        httpx.AsyncClient() as client,
        client.stream("POST", url, json=payload, timeout=120.0) as response,
    ):
        if response.status_code != 200:
            yield f"Error: Ollama returned status code {response.status_code}"
            return

        async for line in response.aiter_lines():
            if line:
                data = json.loads(line)
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
