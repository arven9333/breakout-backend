from typing import Annotated

from fastapi import Depends

from service.map.base import MapService
from dependencies.repo.map_service import MAP_REPOSITORY


async def get_map_service(repository: MAP_REPOSITORY):
    return MapService(
        repo=repository
    )


MAP_SERVICE_DEP = Annotated[MapService, Depends(get_map_service)]
