import logging

from sqlalchemy import select, delete, update, insert

from _logging.base import setup_logging
from enums.figure import FigureEnum

from repositories.base import SQLAlchemyRepo
from models.maps.base import IconMetricFigure

logger = logging.getLogger(__name__)
setup_logging(__name__)


class FigureServiceRepository(SQLAlchemyRepo):
    async def add_figure(
            self,
            map_level_id: int,
            coord_x: float | None = None,
            coord_y: float | None = None,
            color: str | None = None,
            content: str | None = None,
            type: str | None = None,
            radius: float | None = None,
            radius_color: float | None = None,
            bounds: dict | None = None,
            latlngs: dict | None = None,
    ) -> dict:
        icon_metric_figure = IconMetricFigure(
            coord_x=coord_x,
            coord_y=coord_y,
            color=color,
            content=content,
            type=type,
            map_level_id=map_level_id,
            bounds=bounds,
            latlngs=latlngs,
            radius=radius,
            radius_color=radius_color
        )

        async with self.session as session:
            await session.add(icon_metric_figure)

            await session.flush()

            data = {
                "id": icon_metric_figure.id,
                "map_level_id": icon_metric_figure.map_level_id,
                "coord_x": icon_metric_figure.coord_x,
                "coord_y": icon_metric_figure.coord_y,
                "color": icon_metric_figure.color,
                "content": icon_metric_figure.content,
                "type": icon_metric_figure.type,
                "bounds": icon_metric_figure.bounds,
                "latlngs": icon_metric_figure.latlngs,
                "radius": icon_metric_figure.radius,
                "radius_color": icon_metric_figure.radius_color,
            }
        return data

    async def update_figure(
            self,
            icon_metric_figure_id: int,
            map_level_id: int,
            coord_x: float | None = None,
            coord_y: float | None = None,
            color: str | None = None,
            content: str | None = None,
            type: str | None = None,
            radius: float | None = None,
            radius_color: float | None = None,
            bounds: dict | None = None,
            latlngs: dict | None = None,

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
            bounds=bounds,
            latlngs=latlngs,
            radius=radius,
            radius_color=radius_color
        ).where(
            IconMetricFigure.id == icon_metric_figure_id,
        ).returning(IconMetricFigure)

        data = None
        async with self.session as session:
            res = await session.execute(stmt)

            icon_metric_figure = res.scalar_one()
            data = {
                "icon_metric_figure_id": icon_metric_figure.id,
                "map_level_id": icon_metric_figure.map_level_id,
                "coord_x": icon_metric_figure.coord_x,
                "coord_y": icon_metric_figure.coord_y,
                "color": icon_metric_figure.color,
                "content": icon_metric_figure.content,
                "type": icon_metric_figure.type,
                "bounds": icon_metric_figure.bounds,
                "latlngs": icon_metric_figure.latlngs,
                "radius": icon_metric_figure.radius,
                "radius_color": icon_metric_figure.radius_color,
            }
        return data

    async def delete_figure(self, icon_metric_figure_id: int) -> None:
        query = delete(
            IconMetricFigure
        ).where(
            IconMetricFigure.id == icon_metric_figure_id,
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def get_figure_by_id(self, icon_metric_figure_id: int) -> dict | None:
        stmt = select(
            IconMetricFigure
        ).where(
            IconMetricFigure.id == icon_metric_figure_id
        )
        data = None
        async with self.session as session:
            res = await session.execute(stmt)
            icon_metric_figure = res.scalar_one_or_none()
            if icon_metric_figure is not None:
                data = {
                    "icon_metric_figure_id": icon_metric_figure.id,
                    "map_level_id": icon_metric_figure.map_level_id,
                    "coord_x": icon_metric_figure.coord_x,
                    "coord_y": icon_metric_figure.coord_y,
                    "color": icon_metric_figure.color,
                    "content": icon_metric_figure.content,
                    "type": icon_metric_figure.type,
                    "bounds": icon_metric_figure.bounds,
                    "latlngs": icon_metric_figure.latlngs,
                    "radius": icon_metric_figure.radius,
                    "radius_color": icon_metric_figure.radius_color,
                }
        return data
