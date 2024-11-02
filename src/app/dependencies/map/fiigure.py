from typing import Annotated

from fastapi import Depends

from dependencies.repo.figure_service import ICON_FIGURE_REPOSITORY
from service.map.figure import FigureService


async def get_icon_figure_service(repository: ICON_FIGURE_REPOSITORY):
    return FigureService(
        repo=repository
    )


ICON_FIGURE_SERVICE_DEP = Annotated[FigureService, Depends(get_icon_figure_service)]
