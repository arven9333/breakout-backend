import logging

from sqlalchemy import select, delete

from _logging.base import setup_logging

from repositories.base import SQLAlchemyRepo
from models.maps.icons import Icon, IconCategory
from dto.request.map.icon import IconCreateDTO, IconCategoryCreateDTO
from dto.response.map.icon import IconDTO, IconCategoryDTO

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
        icon_category = Icon(
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

    async def get_icons(self) -> list[IconDTO] | None:
        query = (
            select(
                Icon
            )
        )
        async with self.session as session:
            result = await session.execute(query)

            if icons := result.scalars().all():
                return [
                    IconDTO.from_db_model(icon)
                    for icon in icons
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
                return icon
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