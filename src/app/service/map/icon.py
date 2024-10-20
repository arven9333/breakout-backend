from dataclasses import dataclass
from pathlib import Path

from exceptions.map import IconCategoryNotFound, IconNotFound, IconCategoryAlreadyExists
from scheme.request.map.base import ActionScheme
from settings import ICONS_DIR

from starlette.datastructures import UploadFile

from dto.request.map.icon import IconCategoryCreateDTO, IconCreateDTO
from dto.response.map.icon import IconCategoryDTO, IconDTO, CategoryGroupedIcons, CategoryDTO
from repositories.map.icon import IconServiceRepository, IconLevelServiceRepository
from utils.file_operations import upload_file, delete_file


@dataclass
class IconService:
    repo: IconServiceRepository

    async def add_icon(self, icon_create_dto: IconCreateDTO) -> IconDTO:
        category = await self.repo.get_icon_category_by_id(icon_create_dto.category_id)
        if category is None:
            raise IconCategoryNotFound(details="Category not found", error=404)

        icon = await self.repo.add_icon(icon_create_dto)
        return icon

    async def get_icons_list(self) -> list[IconDTO]:
        icons = await self.repo.get_icons_list()
        return icons

    async def add_icon_category(
            self,
            icon_category_create_dto: IconCategoryCreateDTO,
    ) -> IconCategoryDTO:

        exists = await self.repo.get_icon_category_by_name(icon_category_create_dto.name)
        if exists is not None:
            raise IconCategoryAlreadyExists(details=f"Category with this name already exists")

        icon_category = await self.repo.add_icon_category(icon_category_create_dto)
        return icon_category

    async def delete_icon(self, icon_id: int):
        icon = await self.repo.get_icon_by_id(icon_id)
        await delete_file(ICONS_DIR / str(icon.category_id) / icon.image.split('/')[-1])
        await self.repo.delete_icon(icon_id)

    async def delete_category_icon(self, icon_category_id: int):
        category = await self.repo.get_icon_category_by_id(icon_category_id)

        await delete_file(ICONS_DIR / str(category.id))
        await self.repo.delete_icon_category(icon_category_id)

    async def get_category_icon_by_id(self, category_id: int) -> IconCategoryDTO:
        category = await self.repo.get_icon_category_by_id(
            icon_category_id=category_id
        )
        if category is None:
            raise IconCategoryNotFound(details="Category not found", error=404)

        return category

    async def get_icon_by_id(self, icon_id: int) -> IconDTO:
        icon = await self.repo.get_icon_by_id(
            icon_id=icon_id
        )

        if icon is None:
            raise IconNotFound(details="Icon not found", error=404)

        return icon

    async def get_icons(self) -> list[CategoryGroupedIcons]:
        icons = await self.repo.get_icons()
        return icons

    @staticmethod
    async def upload_icon(file: UploadFile, category_id: int, path: Path = ICONS_DIR):
        saved_path = await upload_file(file, path / str(category_id))
        return saved_path

    async def get_categories(self, offset: int = 0, limit: int = 100) -> list[CategoryDTO]:
        data = await self.repo.get_categories(offset=offset, limit=limit)
        return data


@dataclass
class IconLevelActionsService:
    repo: IconLevelServiceRepository

    async def add_icon(
            self,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_level_id: int,
            radius: float | None = None,
            radius_color: str | None = None,

    ) -> dict:
        data = await self.repo.add_icon(coord_x, coord_y, icon_id, map_level_id, radius, radius_color)
        return data

    async def delete_icon(
            self,
            icon_level_id: int
    ):
        await self.repo.delete_icon(icon_level_id)

    async def update_icon(
            self,
            icon_level_id: int,
            coord_x: float,
            coord_y: float,
            icon_id: int,
            map_level_id: int,

    ):
        await self.repo.update_icon(
            icon_level_id=icon_level_id,
            coord_x=coord_x,
            coord_y=coord_y,
            icon_id=icon_id,
            map_level_id=map_level_id,
        )


@dataclass
class ActionsHandleService:
    icon_level_service: IconLevelActionsService

    async def handle_actions(self, actions: list[ActionScheme]):
        for action in actions:
            service = None

            action_type = action.action.value
            action_model = action.type.value

            if action_model == "icon_metric_level":
                service = self.icon_level_service

            if service:
                data = action.data
                match action_type:
                    case "create":
                        await service.add_icon(
                            **data
                        )
                    case "delete":
                        await service.delete_icon(
                            **data
                        )
                    case "update":
                        await service.update_icon(
                            **data
                        )
