import json
import time
import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..services.completions import stream_chat
from ..types.completion import CompletionRequest
from ..utils.response import api_response

completions_router = APIRouter()


@completions_router.post("/completions")
async def chat_completions(request: CompletionRequest):

    if not request.stream:
        return api_response(
            success=False, message="Only streaming is supported right now."
        )

    async def event_generator():
        chat_id = f"chatcompletion-{uuid.uuid4()}"
        created = int(time.time())

        async for text_chunk in stream_chat(request):
            chunk = {
                "id": chat_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": text_chunk},
                        "finish_reason": None,
                    }
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
