from dto.request.user.registration import UserDTO
from dataclasses import dataclass

from models import User


@dataclass
class UserSearchDTO(UserDTO):
    in_party: bool = False

    @classmethod
    def from_db_model(cls, user: User, **kwargs):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            role=user.role,
            raids=user.raids,
            rank=user.rank,
            survival=user.survival,
            hours=user.hours,
            bio=user.hours,
            username_game=user.username_game,
            find_teammates=user.find_teammates,
            in_party=kwargs.get("in_party", False)
        )

