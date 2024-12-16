import logging

from sqlalchemy import select, or_, update, insert, delete

from _logging.base import setup_logging
from dto.request.user.avatar import UserAvatarCreateDTO, UserAvatarUpdateDTO
from dto.response.user.avatar import UserAvatarDTO
from models.user.base import UserAvatar

from repositories.base import SQLAlchemyRepo
from models.user import User
from dto.request.user.registration import UserCreateDTO, UserDTO, UserDBDTO, UserUpdateDTO

logger = logging.getLogger(__name__)
setup_logging(__name__)


class UserServiceRepository(SQLAlchemyRepo):
    async def add_user(
            self,
            user_create_dto: UserCreateDTO
    ) -> UserDTO:

        user = User(
            **user_create_dto.get_user_db_create()
        )
        async with self.session as session:
            await session.add(user)
            await session.flush()

            return UserDTO.from_db_model(user)

    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        query = select(
            User
        ).where(
            User.id == user_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar():
                return UserDTO.from_db_model(user)
            return None

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        query = (
            select(
                User
            ).where(
                User.email == email
            )
        )

        async with self.session as session:
            result = await session.execute(query)
            if user := result.scalar():
                return UserDTO.from_db_model(user)
            return None

    async def update_user(self, user_update_dto: UserUpdateDTO, user_id: int) -> UserDTO | None:
        query = update(
            User
        ).values(
            user_update_dto.as_dict(exclude_none=True)
        ).where(
            User.id == user_id
        ).returning(User)
        async with self.session as session:
            res = await session.execute(query)

            if user := res.scalar_one_or_none():
                return UserDTO.from_db_model(user)
        return

    async def get_user_by_username(self, username: str) -> UserDTO | None:
        query = (
            select(
                User
            ).where(
                User.username == username
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar():
                return UserDTO.from_db_model(user)
            return None

    async def get_user_db_by_id(self, user_id: int) -> UserDBDTO | None:
        query = select(
            User
        ).where(
            User.id == user_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar():
                return UserDBDTO.from_db_model(user)
            return None

    async def get_user_db_by_email(self, email: str) -> UserDBDTO | None:
        query = (
            select(
                User
            ).where(
                User.email == email
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar():
                return UserDBDTO.from_db_model(user)
            return None

    async def get_user_db_by_username(self, username: str) -> UserDBDTO | None:
        query = (
            select(
                User
            ).where(
                User.username == username
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar():
                return UserDBDTO.from_db_model(user)
            return None

    async def get_user_by_external_id(self, external_id: int) -> UserDTO | None:
        query = (
            select(
                User
            ).where(
                User.external_id == external_id
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                return UserDTO.from_db_model(user)
            return None

    async def get_user_db_by_subject(self, subject: str) -> UserDBDTO | None:
        query = select(
            User
        ).where(
            or_(
                User.email == subject,
                User.username == subject,
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                return UserDBDTO.from_db_model(user)
        return None

    async def create_avatar(self, user_create_avatar_dto: UserAvatarCreateDTO) -> UserAvatarDTO:
        stmt = insert(
            UserAvatar
        ).values(
            user_create_avatar_dto.as_dict()
        ).returning(UserAvatar)

        async with self.session as session:
            result = await session.execute(stmt)

            avatar = result.scalar_one()

            return UserAvatarDTO.model_to_dto(avatar)

    async def get_avatar_by_user_id(self, user_id: int) -> UserAvatarDTO | None:
        stmt = select(
            UserAvatar
        ).where(
            UserAvatar.user_id == user_id
        )
        async with self.session as session:
            result = await session.execute(stmt)

            if avatar := result.scalar_one_or_none():
                return UserAvatarDTO.model_to_dto(avatar)
            return

    async def update_avatar(self, user_avatar_update_dto: UserAvatarUpdateDTO, user_id: int) -> UserAvatarDTO:
        stmt = update(
            UserAvatar
        ).values(
            user_avatar_update_dto.as_dict(exclude_none=True)
        ).returning(
            UserAvatar
        )

        async with self.session as session:
            result = await session.execute(stmt)

            avatar = result.scalar_one()

            return UserAvatarDTO.model_to_dto(avatar)

    async def delete_avatar(self, user_id: int) -> UserAvatarDTO | None:
        stmt = delete(
            UserAvatar
        ).where(
            UserAvatar.user_id == user_id
        )
        async with self.session as session:
            result = await session.execute(stmt)

            if avatar := result.scalar_one_or_none():
                return UserAvatarDTO.model_to_dto(avatar)
            return
