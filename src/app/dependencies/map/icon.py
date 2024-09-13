from typing import Annotated

from fastapi import Depends

from service.map.icon import IconService
from dependencies.repo.icon_service import ICON_REPOSITORY


async def get_icon_service(repository: ICON_REPOSITORY):
    return IconService(
        repo=repository
    )

ICON_SERVICE_DEP = Annotated[IconService, Depends(get_icon_service)]