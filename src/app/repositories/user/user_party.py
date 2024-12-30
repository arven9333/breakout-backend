from sqlalchemy import (
    select,
    insert,
    update,
    or_
)

import logging

from sqlalchemy.orm import selectinload, joinedload

from _logging.base import setup_logging
from dto.request.user.registration import UserDTO, AvatarDTO
from dto.response.base import PaginationBaseDTO
from dto.response.user.party import UserPartyDTO, LastUserMessageDTO, UserInvitationDTO, UserInvitationGroupDTO, \
    UserMessageDTO
from enums.status import InvitationStatusEnum
from models import User

from repositories.base import SQLAlchemyRepo
from dto.request.user.party import UserPartyAddDTO, UserMessageAddDTO, InvitationAddDTO, UserPartyReadDTO
from models.user.user_party import Invitation, UserMessages, UserParty

logger = logging.getLogger(__name__)
setup_logging(__name__)


class UserPartyRepository(SQLAlchemyRepo):
    async def insert_user_party(self, user_party_add_dto: UserPartyAddDTO) -> UserPartyDTO | None:
        query = insert(
            UserParty
        ).values(
            **user_party_add_dto.as_dict()
        ).returning(
            UserParty
        )

        async with self.session as session:
            result = await session.execute(query)
            if user_party := result.scalar_one():
                return UserPartyDTO.model_to_dto(user_party)
        return

    async def insert_invitation(self, invitation_add_dto: InvitationAddDTO) -> UserInvitationDTO | None:
        query = insert(
            Invitation
        ).values(
            **invitation_add_dto.as_dict()
        ).returning(
            Invitation
        ).options(
            selectinload(
                Invitation.from_user
            ),
            selectinload(
                Invitation.to_user
            )
        )

        async with self.session as session:
            result = await session.execute(query)
            if invitation := result.scalar_one():
                return UserInvitationDTO.model_to_dto(
                    invitation,
                    from_user=UserDTO.from_db_model(invitation.from_user),
                    to_user=UserDTO.from_db_model(invitation.to_user),
                )
        return

    async def insert_user_messages(self, user_message_add_dto: UserMessageAddDTO) -> UserMessageDTO | None:
        query = insert(
            UserMessages
        ).values(
            **user_message_add_dto.as_dict()
        ).returning(
            UserMessages
        )

        async with self.session as session:
            result = await session.execute(query)
            if user_message := result.scalar_one():
                return UserMessageDTO.model_to_dto(user_message)
        return

    async def read_message(self, party_id: int, user_party_read_dto: UserPartyReadDTO) -> UserPartyDTO | None:

        stmt = update(
            UserParty
        ).values(
            **user_party_read_dto.as_dict(exclude_none=True)
        ).where(
            UserParty.id == party_id
        ).returning(
            UserParty
        )
        async with self.session as session:
            result = await session.execute(stmt)
            if user_party := result.scalar_one():
                return UserPartyDTO.model_to_dto(user_party)
        return

    async def update_invitation(self, invitation_id: int, status: InvitationStatusEnum) -> UserInvitationDTO | None:
        stmt = update(
            Invitation
        ).values(
            status=status
        ).where(
            Invitation.id == invitation_id
        ).returning(Invitation)

        async with self.session as session:
            result = await session.execute(stmt)
            if user_invitation := result.scalar_one():
                return UserInvitationDTO.model_to_dto(user_invitation)
        return

    async def get_user_messages(
            self,
            party_id: int,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[UserMessageDTO], PaginationBaseDTO]:
        stmt = select(
            UserMessages
        ).where(
            UserMessages.user_party_id == party_id
        ).order_by(
            UserMessages.ts_create.desc()
        )

        stmt_count = await self.get_count_from_query(stmt)
        stmt = stmt.limit(limit).offset(offset)

        async with self.session as session:
            result = await session.execute(stmt)
            result_count = await session.execute(stmt_count)
            result_count = result_count.scalar_one_or_none() or 0

            pagination = PaginationBaseDTO(total=result_count, limit=limit, offset=offset)

            if user_messages := result.scalars().all():
                user_messages = [UserMessageDTO.model_to_dto(user_message) for user_message in user_messages]

        return user_messages, pagination

    async def get_user_parties(
            self,
            user_id: int,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[UserPartyDTO], PaginationBaseDTO]:

        stmt = select(
            UserParty
        ).outerjoin(
            UserParty.last_message
        ).where(
            or_(
                UserParty.from_user_id == user_id,
                UserParty.to_user_id == user_id,
            )
        ).options(
            joinedload(UserParty.last_message),
            joinedload(UserParty.from_user),
            joinedload(UserParty.to_user),
            joinedload(UserParty.from_user).joinedload(User.avatar),
            joinedload(UserParty.to_user).joinedload(User.avatar)
        ).distinct()

        stmt_count = await self.get_count_from_query(stmt)
        stmt = stmt.limit(limit).offset(offset)

        result_party = []

        async with self.session as session:
            result = await session.execute(stmt)
            result_count = await self.session.execute(stmt_count)
            result_count = result_count.scalar_one_or_none() or 0

            if user_parties := result.unique().scalars().all():
                for user_party in user_parties:
                    if last_message := user_party.last_message:
                        if last_message.from_user_id == user_id:
                            is_read = True
                        else:
                            field_time = "last_seen_from_user" if user_id == user_party.from_user else "last_seen_to_user"
                            last_seen = getattr(user_party, field_time, None)
                            if last_seen is None or last_message.ts_create > last_seen:
                                is_read = False
                            else:
                                is_read = True

                        last_message = LastUserMessageDTO.model_to_dto(last_message, is_read=is_read)

                    if from_user_avatar := user_party.from_user.avatar:
                        from_user_avatar = AvatarDTO.model_to_dto(from_user_avatar)
                    if to_user_avatar := user_party.to_user.avatar:
                        to_user_avatar = AvatarDTO.model_to_dto(to_user_avatar)

                    user_party_dto = UserPartyDTO.model_to_dto(
                        user_party,
                        last_message=last_message,
                        from_user=UserDTO.from_db_model(user_party.from_user, avatar=from_user_avatar),
                        to_user=UserDTO.from_db_model(user_party.to_user, avatar=to_user_avatar),
                    )
                    result_party.append(
                        user_party_dto
                    )
        pagination = PaginationBaseDTO(total=result_count, limit=limit, offset=offset)
        return result_party, pagination

    async def get_user_invitations(
            self,
            user_id: int,
            mine_sent: bool = False,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[UserInvitationDTO], PaginationBaseDTO]:
        _conditions = []
        if mine_sent is True:
            _conditions.append(Invitation.from_user_id == user_id)
        else:
            _conditions.append(Invitation.to_user_id == user_id)

        stmt = select(
            Invitation
        ).where(
            *_conditions,
            Invitation.status == InvitationStatusEnum.waiting,
        ).options(
            selectinload(Invitation.from_user),
            selectinload(Invitation.to_user),
            selectinload(Invitation.from_user).selectinload(User.avatar),
            selectinload(Invitation.to_user).selectinload(User.avatar),
        ).distinct()

        stmt_count = await self.get_count_from_query(stmt)
        stmt = stmt.limit(limit).offset(offset)

        result_invitations = []

        async with self.session as session:
            result = await session.execute(stmt)
            result_count = await session.execute(stmt_count)
            result_count = result_count.scalar_one_or_none() or 0

            if user_invitations := result.unique().scalars().all():
                for user_invitation in user_invitations:
                    if from_user_avatar := user_invitation.from_user.avatar:
                        from_user_avatar = AvatarDTO.model_to_dto(from_user_avatar)
                    if to_user_avatar := user_invitation.to_user.avatar:
                        to_user_avatar = AvatarDTO.model_to_dto(to_user_avatar)

                    from_user = UserDTO.from_db_model(user_invitation.from_user, avatar=from_user_avatar)
                    to_user = UserDTO.from_db_model(user_invitation.to_user, avatar=to_user_avatar)
                    user_invitation_dto = UserInvitationDTO.model_to_dto(
                        user_invitation,
                        from_user=from_user,
                        to_user=to_user,
                    )
                    result_invitations.append(user_invitation_dto)

        pagination = PaginationBaseDTO(total=result_count, offset=offset, limit=limit)
        return result_invitations, pagination

    async def get_party_by_id(self, party_id: int) -> UserPartyDTO | None:
        stmt = select(
            UserParty
        ).where(
            UserParty.id == party_id
        )

        async with self.session as session:
            result = await session.execute(stmt)
            if user_party := result.scalar_one_or_none():
                return UserPartyDTO.model_to_dto(user_party)
        return

    async def get_invitation_by_id(self, invitation_id: int) -> UserPartyDTO | None:
        stmt = select(
            Invitation
        ).where(
            Invitation.id == invitation_id
        )

        async with self.session as session:
            result = await session.execute(stmt)
            if invitation := result.scalar_one_or_none():
                return UserInvitationDTO.model_to_dto(invitation)
        return

    async def get_invitation_by_users(self, user_id: int, to_user_id: int) -> UserInvitationDTO | None:
        stmt = select(
            Invitation
        ).where(
            Invitation.from_user_id.in_((user_id, to_user_id)),
            Invitation.to_user_id.in_((user_id, to_user_id)),
            Invitation.status != InvitationStatusEnum.canceled,
        ).options(
            selectinload(Invitation.party)
        ).distinct().limit(1)

        async with self.session as session:
            result = await session.execute(stmt)
            if invitation := result.scalar_one_or_none():
                return UserInvitationDTO.model_to_dto(invitation, party_id=getattr(invitation.party, "id", None))
        return
