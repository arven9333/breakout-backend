import logging

from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload

from _logging.base import setup_logging

from repositories.base import SQLAlchemyRepo
from models.maps.base import Icon, IconCategory, IconMetricLayer, IconMetricLevel
from dto.request.map.icon import IconCreateDTO, IconCategoryCreateDTO
from dto.response.map.icon import IconDTO, IconCategoryDTO, CategoryGroupedIcons, IconGroupDTO

logger = logging.getLogger(__name__)
setup_logging(__name__)


class IconServiceRepository(SQLAlchemyRepo):
    async def add_icon(
            self,
            icon_create_dto: IconCreateDTO
    ) -> IconDTO:

        icon = Icon(
            **icon_create_dto.as_dict()
        )
        async with self.session as session:
            await session.add(icon)
            await session.flush()

            return IconDTO.from_db_model(icon)

    async def add_icon_category(self, icon_category_create_dto: IconCategoryCreateDTO) -> IconCategoryDTO | None:
        icon_category = IconCategory(
            **icon_category_create_dto.as_dict()
        )
        async with self.session as session:
            await session.add(icon_category)
            await session.flush()

            return IconCategoryDTO.from_db_model(icon_category)

    async def get_icon_category_by_id(self, icon_category_id: int) -> IconCategoryDTO | None:
        query = (
            select(
                IconCategory
            ).where(
                IconCategory.id == icon_category_id
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if icon_category := result.scalar():
                return IconCategoryDTO.from_db_model(icon_category)
            return None

    async def get_icon_category_by_name(self, icon_category_name: str) -> IconCategoryDTO | None:
        query = (
            select(
                IconCategory
            ).where(
                IconCategory.name == icon_category_name
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if icon_category := result.scalar():
                return IconCategoryDTO.from_db_model(icon_category)
            return None

    async def get_icons(self) -> list[CategoryGroupedIcons] | None:
        query = (
            select(
                IconCategory
            ).outerjoin(
                IconCategory.icons
            ).options(
                joinedload(IconCategory.icons)
            )
        )
        async with self.session as session:
            result = await session.execute(query)

            if categories := result.unique().scalars().all():
                return [
                    CategoryGroupedIcons(
                        category=IconCategoryDTO.from_db_model(category),
                        icons=[
                            IconGroupDTO.from_db_model(icon)
                            for icon in category.icons
                        ]
                    )
                    for category in categories
                ]
            return None

    async def get_icon_by_id(self, icon_id: int) -> IconDTO | None:
        query = select(
            Icon
        ).where(
            Icon.id == icon_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if icon := result.scalar_one():
                return IconDTO.from_db_model(icon)
            return None

    async def delete_icon(self, icon_id: int):
        query = delete(
            Icon
        ).where(
            Icon.id == icon_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def delete_icon_category(self, icon_category_id: int):
        query = delete(
            Icon
        ).where(
            IconCategory.id == icon_category_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()


class IconLayerServiceRepository(SQLAlchemyRepo):
    async def add_icon(
            self,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_layer_id: int
    ):
        icon = IconMetricLayer(
            coord_x=coord_x,
            coord_y=coord_y,
            icon_id=icon_id,
            map_layer_id=map_layer_id,
        )

        async with self.session as session:
            await session.add(icon)
            await session.flush()

            return {
                "id": icon.id,
                "coord_x": icon.coord_x,
                "coord_y": icon.coord_y,
                "map_layer_id": icon.map_layer_id
            }

    async def delete_icon(self, icon_layer_id: int):
        query = delete(
            IconMetricLayer
        ).where(
            id=icon_layer_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def update_icon(
            self,
            icon_layer_id: int,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_layer_id: int,
    ):
        query = update(
            IconMetricLayer
        ).where(
            IconMetricLayer.id == icon_layer_id
        ).values(
            coord_x=coord_x,
            coord_y=coord_y,
            icon_id=icon_id,
            map_layer_id=map_layer_id,
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()


class IconLevelServiceRepository(SQLAlchemyRepo):
    async def add_icon(
            self,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_level_id: int
    ):
        icon = IconMetricLevel(
            coord_x=coord_x,
            coord_y=coord_y,
            icon_id=icon_id,
            map_level_id=map_level_id,
        )

        async with self.session as session:
            await session.add(icon)
            await session.flush()

            return {
                "id": icon.id,
                "coord_x": icon.coord_x,
                "coord_y": icon.coord_y,
                "map_level_id": icon.map_level_id,
            }

    async def delete_icon(self, icon_level_id: int):
        query = delete(
            IconMetricLevel
        ).where(
            id=icon_level_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def update_icon(
            self,
            icon_level_id: int,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_level_id: int,
    ):
        query = update(
            IconMetricLevel
        ).where(
            IconMetricLevel.id == icon_level_id
        ).values(
            coord_x=coord_x,
            coord_y=coord_y,
            icon_id=icon_id,
            map_level_id=map_level_id,
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()
