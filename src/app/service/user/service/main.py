from dataclasses import dataclass
from dto.request.user.registration import UserCreateDTO, UserDTO
from repositories.user.user_service import UserServiceRepository
from service.user.service.service_abc import UserServiceABC
from exceptions.user import UserEmailAlreadyExists, UserUsernameAlreadyExists


@dataclass
class UserService(UserServiceABC):
    repo: UserServiceRepository

    async def create_user(self, user: UserCreateDTO) -> UserDTO:
        if await self.repo.get_user_by_email(user.email):
            raise UserEmailAlreadyExists
        if await self.repo.get_user_by_username(user.username):
            raise UserUsernameAlreadyExists

        user = await self.repo.add_user(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        return await self.repo.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        return await self.repo.get_user_by_email(email)

    async def get_user_by_username(self, username: str) -> UserDTO | None:
        return await self.repo.get_user_by_username(username)
