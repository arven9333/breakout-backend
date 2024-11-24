from dataclasses import dataclass
from enums.roles import UserRole
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

    async def get_user_by_id(self, user_id: int, need_exception: bool = False) -> UserDTO:
        user = await self.repo.get_user_by_id(user_id)
        if user is None and need_exception is True:
            raise HTTPException(status_code=404, detail="User not found")
        return user

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

    async def check_user_role(self, user_id: int, available_roles: list[str], need_exception: bool = True):
        user = await self.get_user_by_id(user_id, need_exception=need_exception)

        if user is None:
            return False

        if user.role not in available_roles:
            if need_exception is True:
                raise HTTPException(status_code=403, detail="Access denied (bad privilege)")
            return False
        return True

    async def admin_role_required(self, user_id: int):
        roles = [UserRole.admin.value]
        return await self.check_user_role(user_id, roles, need_exception=True)

    async def premium_user_role_required(self, user_id: int):
        roles = [UserRole.premium.value]
        return await self.check_user_role(user_id, roles, need_exception=True)

    async def no_default_role_required(self, user_id: int):
        roles = [UserRole.premium.value]
        return await self.check_user_role(user_id, roles, need_exception=True)
