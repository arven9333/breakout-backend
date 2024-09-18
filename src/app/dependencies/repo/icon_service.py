from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.map.icon import (
    IconServiceRepository,
    IconLevelServiceRepository,
)


async def get_icon_repository(session: MasterSessionMakerDep):
    return IconServiceRepository(
        session=session
    )


async def get_icon_level_repository(session: MasterSessionMakerDep):
    return IconLevelServiceRepository(
        session=session
    )


ICON_REPOSITORY = Annotated[IconServiceRepository, Depends(get_icon_repository)]
ICON_LEVEL_REPOSITORY = Annotated[IconLevelServiceRepository, Depends(get_icon_level_repository)]
