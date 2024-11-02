import logging

from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import joinedload

from _logging.base import setup_logging
from enums.figure import FigureEnum

from repositories.base import SQLAlchemyRepo
from models.maps.base import IconMetricFigure

logger = logging.getLogger(__name__)
setup_logging(__name__)


class FigureServiceRepository(SQLAlchemyRepo):
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
        stmt = insert(
            IconMetricFigure
        ).values(
            coord_x=coord_x,
            coord_y=coord_y,
            color=color,
            content=content,
            type=type,
            map_level_id=map_level_id,
            bold=bold
        ).returning(IconMetricFigure)

        async with self.session as session:
            res = await session.execute(stmt)
            await session.flush()
            await session.commit()
            icon_metric_figure = res.scalar_one()
            return {
                "id": icon_metric_figure.id,
                "map_level_id": icon_metric_figure.map_level_id,
                "coord_x": icon_metric_figure.coord_x,
                "coord_y": icon_metric_figure.coord_y,
                "color": icon_metric_figure.color,
                "content": icon_metric_figure.content,
                "type": icon_metric_figure.type,
                "bold": icon_metric_figure.bold,
            }

    async def update_figure(
            self,
            icon_metric_figure_id: int,
            coord_x: float,
            coord_y: float,
            color: str,
            content: str,
            map_level_id: int,
            type: str = FigureEnum.circle,
            bold: bool = False,

    ) -> dict:
        stmt = update(
            IconMetricFigure
        ).values(
            coord_x=coord_x,
            coord_y=coord_y,
            color=color,
            content=content,
            type=type,
            map_level_id=map_level_id,
            bold=bold
        ).where(
            IconMetricFigure.id == icon_metric_figure_id,
        ).returning(IconMetricFigure)

        async with self.session as session:
            res = await session.execute(stmt)
            await session.flush()
            await session.commit()
            icon_metric_figure = res.scalar_one()
            return {
                "icon_metric_figure_id": icon_metric_figure.id,
                "map_level_id": icon_metric_figure.map_level_id,
                "coord_x": icon_metric_figure.coord_x,
                "coord_y": icon_metric_figure.coord_y,
                "color": icon_metric_figure.color,
                "content": icon_metric_figure.content,
                "type": icon_metric_figure.type,
                "bold": icon_metric_figure.bold,
            }

    async def delete(self, icon_metric_figure_id: int) -> dict:
        stmt = delete(
            IconMetricFigure
        ).where(
            IconMetricFigure.id == icon_metric_figure_id
        ).returning(
            IconMetricFigure
        )

        async with self.session as session:
            res = await session.execute(stmt)
            await session.flush()
            await session.commit()
            icon_metric_figure = res.scalar_one()
            return {
                "icon_metric_figure_id": icon_metric_figure.id,
                "map_level_id": icon_metric_figure.map_level_id,
                "coord_x": icon_metric_figure.coord_x,
                "coord_y": icon_metric_figure.coord_y,
                "color": icon_metric_figure.color,
                "content": icon_metric_figure.content,
                "type": icon_metric_figure.type,
                "bold": icon_metric_figure.bold,
            }

    async def get_figure_by_id(self, icon_metric_figure_id: int) -> dict | None:
        stmt = select(
            IconMetricFigure
        ).where(
            IconMetricFigure.id == icon_metric_figure_id
        )

        async with self.session as session:
            res = await session.execute(stmt)
            icon_metric_figure = res.scalar_one_or_none()
            if icon_metric_figure is not None:
                return {
                    "icon_metric_figure_id": icon_metric_figure.id,
                    "map_level_id": icon_metric_figure.map_level_id,
                    "coord_x": icon_metric_figure.coord_x,
                    "coord_y": icon_metric_figure.coord_y,
                    "color": icon_metric_figure.color,
                    "content": icon_metric_figure.content,
                    "type": icon_metric_figure.type,
                    "bold": icon_metric_figure.bold,
                }
        return
