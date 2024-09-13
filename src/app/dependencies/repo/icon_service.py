from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.map.icon import IconServiceRepository


async def get_icon_repository(session: MasterSessionMakerDep):
    return IconServiceRepository(
        session=session
    )

ICON_REPOSITORY = Annotated[IconServiceRepository, Depends(get_icon_repository)]