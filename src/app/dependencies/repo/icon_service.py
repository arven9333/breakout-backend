from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.map.icon import (
    IconServiceRepository,
    IconLayerServiceRepository,
    IconLevelServiceRepository,
)


async def get_icon_repository(session: MasterSessionMakerDep):
    return IconServiceRepository(
        session=session
    )


async def get_icon_layer_repository(session: MasterSessionMakerDep):
    return IconLayerServiceRepository(
        session=session
    )


async def get_icon_level_repository(session: MasterSessionMakerDep):
    return IconLevelServiceRepository(
        session=session
    )


ICON_REPOSITORY = Annotated[IconServiceRepository, Depends(get_icon_repository)]
ICON_LAYER_REPOSITORY = Annotated[IconLayerServiceRepository, Depends(get_icon_layer_repository)]
ICON_LEVEL_REPOSITORY = Annotated[IconLevelServiceRepository, Depends(get_icon_level_repository)]
