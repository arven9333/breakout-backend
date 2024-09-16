from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.map.base import MapServiceRepository


async def get_map_repository(session: MasterSessionMakerDep):
    return MapServiceRepository(
        session=session
    )


MAP_REPOSITORY = Annotated[MapServiceRepository, Depends(get_map_repository)]
