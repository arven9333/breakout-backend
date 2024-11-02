from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.map.figure import FigureServiceRepository


async def get_icon_figure_repository(session: MasterSessionMakerDep):
    return FigureServiceRepository(
        session=session
    )


ICON_FIGURE_REPOSITORY = Annotated[FigureServiceRepository, Depends(get_icon_figure_repository)]
