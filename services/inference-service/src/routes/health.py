from fastapi import APIRouter

from ..config.constant import api_response

health_router = APIRouter()


@health_router.get("/")
async def health_check():
    return api_response(
        success=True,
        message="Inference service is up and running",
    )
