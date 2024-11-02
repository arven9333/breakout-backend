from dataclasses import dataclass
from pathlib import Path

from enums.figure import FigureEnum
from exceptions.map import IconCategoryNotFound, IconNotFound, IconCategoryAlreadyExists
from scheme.request.map.base import ActionScheme
from settings import ICONS_DIR

from starlette.datastructures import UploadFile

from dto.request.map.icon import IconCategoryCreateDTO, IconCreateDTO
from dto.response.map.icon import IconCategoryDTO, IconDTO, CategoryGroupedIcons, CategoryDTO
from repositories.map.figure import FigureServiceRepository
from utils.file_operations import upload_file, delete_file


@dataclass
class FigureService:
    repo: FigureServiceRepository

    async def add_figure(
            self,
            coord_x: float,
            coord_y: float,
            color: str,
            content: str,
            map_level_id: int,
            type: str = FigureEnum.circle,
            bold: bool = False,
    ) -> dict:

        figure = await self.repo.add_figure(
            coord_x=coord_x,
            coord_y=coord_y,
            color=color,
            content=content,
            type=type,
            map_level_id=map_level_id,
            bold=bold
        )
        return figure

    async def update_figure(
            self,
            icon_metric_figure_id: int,
            coord_x: float,
            coord_y: float,
            color: str,
            content: str,
            map_level_id: int,
            type: str = FigureEnum.circle,
            bold: int = 0,
    ) -> dict | None:

        has_figure = await self.repo.get_figure_by_id(
            icon_metric_figure_id=icon_metric_figure_id
        )
        if has_figure is not None:
            bold = bool(bold) if bold in (0, 1) else False

            figure = await self.repo.update_figure(
                icon_metric_figure_id=icon_metric_figure_id,
                coord_x=coord_x,
                coord_y=coord_y,
                color=color,
                content=content,
                type=type,
                map_level_id=map_level_id,
                bold=bold
            )
            return figure
        return

    async def delete_figure(self, icon_metric_figure_id: int) -> dict | None:
        has_figure = await self.repo.get_figure_by_id(
            icon_metric_figure_id=icon_metric_figure_id
        )
        if has_figure is not None:
            deleted = await self.repo.delete(icon_metric_figure_id)
            return deleted
        return

    async def match_action(self, action_type: str, **kwargs):
        match action_type:
            case "create":
                await self.add_figure(
                    **kwargs
                )
            case "delete":
                await self.delete_figure(
                    **kwargs
                )
            case "update":
                await self.update_figure(
                    **kwargs
                )
