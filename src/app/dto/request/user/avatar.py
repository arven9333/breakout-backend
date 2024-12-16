from dto.base import DTO
from dataclasses import dataclass


@dataclass
class UserAvatarCreateDTO(DTO):
    user_id: int
    zoom: int = 1
    alignment: int = 1
    image: str | None = None


@dataclass
class UserAvatarUpdateDTO(DTO):
    image: str | None = None
    zoom: int | None = None
    alignment: int | None = None
