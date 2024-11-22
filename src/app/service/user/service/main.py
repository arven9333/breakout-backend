from dataclasses import dataclass

from fastapi import HTTPException

from dto.request.user.registration import UserCreateDTO, UserDTO, UserDBDTO, UserUpdateDTO
from repositories.user.user_service import UserServiceRepository
from service.user.service.service_abc import UserServiceABC


@dataclass
class UserService(UserServiceABC):
    repo: UserServiceRepository

    async def create_user(self, user: UserCreateDTO) -> UserDTO:
        if user.email and await self.repo.get_user_by_email(user.email):
            raise HTTPException(status_code=422, detail="User with this email already exists")
        if await self.repo.get_user_by_username(user.username):
            raise HTTPException(status_code=422, detail="User with this username already exists")

        user = await self.repo.add_user(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        return await self.repo.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        return await self.repo.get_user_by_email(email)

    async def get_user_by_username(self, username: str) -> UserDTO | None:
        return await self.repo.get_user_by_username(username)

    async def get_user_db_by_id(self, user_id: int) -> UserDBDTO:
        return await self.repo.get_user_db_by_id(user_id)

    async def get_user_db_by_email(self, email: str) -> UserDBDTO | None:
        return await self.repo.get_user_db_by_email(email)

    async def get_user_db_by_subject(self, subject: str) -> UserDBDTO | None:
        return await self.repo.get_user_db_by_subject(subject)

    async def get_user_db_by_username(self, username: str) -> UserDBDTO | None:
        return await self.repo.get_user_db_by_username(username)

    async def get_user_by_external_id(self, external_id: int) -> UserDTO:
        return await self.repo.get_user_by_external_id(external_id)

    async def update_user(self, user_update_dto: UserUpdateDTO, user_id: int) -> UserDTO:
        return await self.repo.update_user(user_update_dto, user_id)
