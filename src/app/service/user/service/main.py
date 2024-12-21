from dataclasses import dataclass

from starlette.datastructures import UploadFile

from dto.request.user.avatar import UserAvatarCreateDTO, UserAvatarUpdateDTO
from dto.response.user.avatar import UserAvatarDTO
from dto.response.user.base import UserSearchDTO
from enums.roles import UserRole
from fastapi import HTTPException

from dto.request.user.registration import UserCreateDTO, UserDTO, UserDBDTO, UserUpdateDTO
from repositories.user.user_service import UserServiceRepository
from service.user.service.service_abc import UserServiceABC
from settings import AVATARS_DIR, SRC_DIR
from utils.file_operations import save_upload_file, delete_file, create_dirs


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

    async def create_avatar(self, user_create_avatar_dto: UserAvatarCreateDTO, file: UploadFile) -> UserAvatarDTO:
        extension = file.filename.rsplit('.', 1)[-1]
        path = AVATARS_DIR / (str(user_create_avatar_dto.user_id) + '.' + extension)

        has_avatar = await self.get_avatar_by_user_id(user_create_avatar_dto.user_id)

        if has_avatar:
            raise HTTPException(status_code=422, detail="Avatar already exists")

        try:
            create_dirs(AVATARS_DIR)
            path = save_upload_file(upload_file=file, destination=path)
            user_create_avatar_dto.image = path
            avatar_dto = await self.repo.create_avatar(user_create_avatar_dto)
        except Exception as e:
            await delete_file(path=path)
            raise HTTPException(status_code=500, detail="Error while creating avatar")

        return avatar_dto

    async def update_avatar(self, user_avatar_update_dto: UserAvatarUpdateDTO, user_id: int,
                            file: UploadFile | None = None) -> UserAvatarDTO:

        user_avatar_dto = await self.get_avatar_by_user_id(user_id, raise_exception=True)

        path_delete = SRC_DIR / user_avatar_dto.image
        if file:

            extension = file.filename.rsplit('.', 1)[-1]
            path = AVATARS_DIR / (str(user_id) + '.' + extension)
            await delete_file(path_delete)
            path = save_upload_file(upload_file=file, destination=path)

            user_avatar_update_dto.image = path

        return await self.repo.update_avatar(user_avatar_update_dto, user_id)

    async def get_avatar_by_user_id(self, user_id: int, raise_exception=False) -> UserAvatarDTO | None:
        avatar_dto = await self.repo.get_avatar_by_user_id(user_id)

        if raise_exception is True and avatar_dto is None:
            raise HTTPException(status_code=404, detail="Avatar not found")
        return avatar_dto

    async def delete_avatar(self, user_id: int):

        path = AVATARS_DIR / str(user_id)

        await self.get_avatar_by_user_id(user_id, raise_exception=True)

        await delete_file(path)
        return await self.repo.delete_avatar(user_id)

    async def search_users(
            self,
            user_id: int,
            raids: str | None = None,
            hours: str | None = None,
            rank: str | None = None,
            stars: str | None = None,
            query_search: str | None = None,
            damage: str | None = None,
            limit: int = 100,
            offset: int = 0,
    ) -> tuple[list[UserSearchDTO], int]:

        data, total = await self.repo.search_users(
            user_id=user_id,
            raids=raids,
            hours=hours,
            rank=rank,
            damage=damage,
            query_search=query_search,
            stars=stars,
            limit=limit,
            offset=offset,
        )
        return data, total
