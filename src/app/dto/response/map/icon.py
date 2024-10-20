from typing import Optional

from dto.base import DTO
from dataclasses import dataclass
from models.maps.base import Icon, IconCategory


@dataclass
class IconCategoryDTO(DTO):
    id: int
    name: str

    @classmethod
    def from_db_model(cls, icon_category: IconCategory):
        return cls(
            id=icon_category.id,
            name=icon_category.name,
        )


@dataclass
class CategoryDTO(DTO):
    id: int
    name: str


@dataclass
class IconDTO(DTO):
    id: int
    name: str
    image: str
    category_id: int

    @classmethod
    def from_db_model(cls, icon: Icon):
        return cls(
            id=icon.id,
            name=icon.name,
            image=icon.image,
            category_id=icon.category_id
        )


@dataclass
class IconGroupDTO(DTO):
    id: int
    name: str
    image: str

    @classmethod
    def from_db_model(cls, icon: Icon):
        return cls(
            id=icon.id,
            name=icon.name,
            image=icon.image,
        )


@dataclass
class CategoryGroupedIcons(DTO):
    category: IconCategoryDTO
    icons: Optional[list[IconGroupDTO]]
