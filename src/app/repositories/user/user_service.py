import logging

from sqlalchemy import select

from _logging.base import setup_logging

from repositories.base import SQLAlchemyRepo
from models.user import User
from dto.request.user.registration import UserCreateDTO, UserDTO

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
