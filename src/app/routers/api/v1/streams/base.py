from fastapi import APIRouter

from dependencies.streams.base import STREAMER_SERVICE_DEP
from scheme.response.common import BooleanResponse
from settings import STREAMER_NAME

router = APIRouter(tags=["streams.v1.base"])


@router.get('/is_streaming', response_model=BooleanResponse)
async def is_streaming(
        stream_service: STREAMER_SERVICE_DEP,
        name: str = STREAMER_NAME,
):
    is_streaming_ = await stream_service.is_streaming(name)

    return {
        "status": is_streaming_
    }
