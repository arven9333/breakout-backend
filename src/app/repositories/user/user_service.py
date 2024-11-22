import logging

from sqlalchemy import select, or_, update

from _logging.base import setup_logging

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
