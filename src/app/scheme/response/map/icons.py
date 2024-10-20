from typing import Optional

from pydantic import BaseModel


class ConfigBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class IconScheme(BaseModel):
    id: int
    image: str
    category_id: int
    name: str


class IconCategoryScheme(BaseModel):
    id: int
    name: str


class IconGroupedScheme(ConfigBaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: id
    name: str
    image: str


class CategoryGroupedIconsScheme(ConfigBaseModel):
    category: IconCategoryScheme
    icons: Optional[list[IconGroupedScheme]]


class CategoryScheme(BaseModel):
    id: int
    name: str


class CategoryResponseScheme(BaseModel):
    categories: list[CategoryScheme]


class CategoryGroupedIconsResponseScheme(ConfigBaseModel):
    data: Optional[list[CategoryGroupedIconsScheme]]


class IconSchemeResponse(BaseModel):
    icons: list[IconScheme]
