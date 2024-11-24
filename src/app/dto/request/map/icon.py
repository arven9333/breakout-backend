from dto.base import DTO
from dataclasses import dataclass


@dataclass
class IconCategoryCreateDTO(DTO):
    name: str


@dataclass
class IconCreateDTO(DTO):
    category_id: int
    name: str
    image: str
