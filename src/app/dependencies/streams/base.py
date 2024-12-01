from fastapi import Depends
from typing import Annotated
from service.streams.streamer import StreamerService


def get_streamer_service() -> StreamerService:
    return StreamerService()


STREAMER_SERVICE_DEP = Annotated[StreamerService, Depends(get_streamer_service)]
