from abc import ABC
from dataclasses import dataclass
from repositories.user.user_service import UserServiceRepository
from dto.request.user.registration import UserCreateDTO, UserDTO


@dataclass
class UserServiceABC(ABC):
    repo: UserServiceRepository

    async def create_user(self, user: UserCreateDTO) -> UserDTO:
        pass

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        pass

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        pass

    async def get_user_by_username(self, username: str) -> UserDTO | None:
        pass
