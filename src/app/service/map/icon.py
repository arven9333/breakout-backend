from dataclasses import dataclass
from pathlib import Path

from exceptions.map import IconCategoryNotFound, IconNotFound, IconCategoryAlreadyExists
from settings import ICONS_DIR, SRC_DIR

from starlette.datastructures import UploadFile

from dto.request.map.icon import IconCategoryCreateDTO, IconCreateDTO
from dto.response.map.icon import IconCategoryDTO, IconDTO, CategoryGroupedIcons
from repositories.map.icon import IconServiceRepository
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
