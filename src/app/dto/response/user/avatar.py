from dto.base import DTO
from dataclasses import dataclass


@dataclass
class UserAvatarDTO(DTO):
    id: int
    user_id: int
    image: str
    zoom: int = 1
    alignment: int = 1
