import logging

from sqlalchemy import select, or_, update, insert, delete
from sqlalchemy.orm import selectinload

from _logging.base import setup_logging
from dto.request.user.avatar import UserAvatarCreateDTO, UserAvatarUpdateDTO
from dto.response.user.avatar import UserAvatarDTO
from dto.response.user.base import UserSearchDTO
from dto.response.user.party import UserInvitationDTO
from enums.status import InvitationStatusEnum
from models.user.base import UserAvatar
from models.user.user_party import Invitation

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
        ).options(
            selectinload(User.avatar)
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto

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
            if user := result.scalar_one_or_none():
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
            ).options(
                selectinload(User.avatar)
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto

            return None

    async def get_user_db_by_id(self, user_id: int) -> UserDBDTO | None:
        query = select(
            User
        ).where(
            User.id == user_id
        ).options(
            selectinload(User.avatar)
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDBDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto

            return None

    async def get_user_db_by_email(self, email: str) -> UserDBDTO | None:
        query = (
            select(
                User
            ).where(
                User.email == email
            ).options(
                selectinload(User.avatar)
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDBDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto
            return None

    async def get_user_db_by_username(self, username: str) -> UserDBDTO | None:
        query = (
            select(
                User
            ).where(
                User.username == username
            ).options(
                selectinload(User.avatar)
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDBDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto
            return None

    async def get_user_by_external_id(self, external_id: int) -> UserDTO | None:
        query = (
            select(
                User
            ).where(
                User.external_id == external_id
            ).options(
                selectinload(User.avatar)
            )
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto
            return None

    async def get_user_db_by_subject(self, subject: str) -> UserDBDTO | None:
        query = select(
            User
        ).where(
            or_(
                User.email == subject,
                User.username == subject,
            )
        ).options(
            selectinload(User.avatar)
        )

        async with self.session as session:
            result = await session.execute(query)

            if user := result.scalar_one_or_none():
                if avatar := user.avatar:
                    avatar = UserAvatarDTO.model_to_dto(avatar)

                user_dto = UserDBDTO.from_db_model(user)
                user_dto.avatar = avatar
                return user_dto
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
        ).where(
            UserAvatar.user_id == user_id
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

    async def search_users(
            self,
            user_id: int,
            raids: str | None = None,
            hours: str | None = None,
            rank: str | None = None,
            stars_from: int | None = None,
            stars_to: int | None = None,
            damage: str | None = None,
            query_search: str | None = None,
            limit: int = 100,
            offset: int = 0,
    ) -> tuple[list[UserSearchDTO], int]:
        def need_invitation(user_id: int, search_user_id: int, from_user_id: int, to_user_id: int):
            if from_user_id == user_id and search_user_id == to_user_id:
                return True
            if from_user_id == search_user_id and user_id == to_user_id:
                return True
            return False

        _conditions = []
        if raids:
            _conditions.append(User.raids == raids)
        if hours:
            _conditions.append(User.hours == hours)
        if rank:
            _conditions.append(User.rank == rank)
        if stars_from:
            _conditions.append(User.stars >= stars_from)
        if stars_to:
            _conditions.append(User.stars <= stars_to)
        if damage:
            _conditions.append(User.damage == damage)
        if query_search:
            _conditions.append(
                or_(
                    User.username.ilike(f"%{query_search}%"),
                    User.username_game.ilike(f"%{query_search}%"),
                    User.email.ilike(f"%{query_search}%"),
                    User.bio.ilike(f"%{query_search}%"),
                )
            )
        stmt_invitation = select(
            Invitation,
        ).where(
            or_(
                Invitation.to_user_id == user_id,
                Invitation.from_user_id == user_id
            ),
            Invitation.status != InvitationStatusEnum.canceled
        ).options(
            selectinload(Invitation.party)
        )
        stmt = select(
            User,
        ).where(
            User.id != user_id,
            User.find_teammates == True,
            *_conditions
        ).options(
            selectinload(User.avatar)
        ).order_by(
            User.username_game
        ).distinct()

        users_search_dto = []

        stmt_count = await self.get_count_from_query(stmt)
        stmt = stmt.limit(limit).offset(offset)

        async with self.session as session:
            result = await session.execute(stmt)
            result_invitation = await session.execute(stmt_invitation)
            result_count = await self.session.execute(stmt_count)

            invitations = result_invitation.scalars().all()
            count = result_count.scalar_one_or_none() or 0

            if users := result.scalars().all():

                for user_search in users:
                    invitation = [
                        inv for inv in invitations
                        if need_invitation(user_id, user_search.id, inv.from_user_id, inv.to_user_id)
                    ]

                    if invitation:
                        party_id = None
                        invitation_base = invitation[0]

                        if invitation_base.status == InvitationStatusEnum.accepted:
                            party_id = invitation_base.party.id

                        invitation = UserInvitationDTO.model_to_dto(invitation_base, party_id=party_id)

                    else:
                        invitation = None

                    users_search_dto.append(
                        UserSearchDTO.from_db_model(
                            user_search,
                            invitation=invitation,
                            avatar=UserAvatarDTO.model_to_dto(user_search.avatar) if user_search.avatar else None,
                        )
                    )

        return users_search_dto, count
