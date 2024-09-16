from dto.base import DTO
from dataclasses import dataclass
from typing import Optional


@dataclass
class IconCategoryCreateDTO(DTO):
    name: str


@dataclass
class IconCreateDTO(DTO):
    category_id: int
    name: str
    image: str
