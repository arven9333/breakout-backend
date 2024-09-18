from typing import Annotated

from fastapi import Depends

from service.map.icon import (
    IconService,
    IconLevelActionsService,
    ActionsHandleService,
)

from dependencies.repo.icon_service import (
    ICON_REPOSITORY,
    ICON_LEVEL_REPOSITORY,
)


async def get_icon_service(repository: ICON_REPOSITORY):
    return IconService(
        repo=repository
    )


async def get_icon_level_service(repository: ICON_LEVEL_REPOSITORY):
    return IconLevelActionsService(
        repo=repository
    )


ICON_SERVICE_DEP = Annotated[IconService, Depends(get_icon_service)]
ICON_LEVEL_SERVICE_DEP = Annotated[IconLevelActionsService, Depends(get_icon_level_service)]


async def get_icon_total_service(
        level_service: ICON_LEVEL_SERVICE_DEP,
):
    return ActionsHandleService(
        icon_level_service=level_service,
    )


ICON_ACTIONS_SERVICE_DEP = Annotated[ActionsHandleService, Depends(get_icon_total_service)]
