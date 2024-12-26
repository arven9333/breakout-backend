from dataclasses import dataclass
from fastapi import HTTPException
from datetime import datetime

from dto.request.user.donation import UserDonationAddDTO, UserDonationUpdateDTO
from dto.response.base import PaginationBaseDTO
from dto.response.user.party import (
    UserPartyDTO,
    UserInvitationDTO,
    UserMessageDTO,
    UserInvitationGroupDTO,
    InvitationTypeEnum,
    InvitationStatusEnum
)
from dto.request.user.party import (
    UserPartyAddDTO,
    UserMessageAddDTO,
    InvitationAddDTO,
    UserPartyReadDTO
)

from repositories.user.user_party import UserPartyRepository
from service.user.service.service_abc import UserServiceABC


@dataclass
class UserPartyService(UserServiceABC):
    repo: UserPartyRepository

    async def insert_user_party(self, user_party_add_dto: UserPartyAddDTO) -> UserPartyDTO | None:
        user_party_dto = await self.repo.insert_user_party(user_party_add_dto)
        return user_party_dto

    async def insert_invitation(self, invitation_add_dto: InvitationAddDTO) -> UserInvitationDTO | None:
        user_invitation = await self.repo.insert_invitation(invitation_add_dto)
        return user_invitation

    async def insert_user_messages(self, user_message_add_dto: UserMessageAddDTO) -> UserMessageDTO | None:
        user_message = await self.repo.insert_user_messages(user_message_add_dto)
        return user_message

    async def get_party_by_id(self, party_id: int, need_exception: bool = False) -> UserPartyDTO | None:
        party_dto = await self.repo.get_party_by_id(party_id)
        if party_dto is None and need_exception is True:
            raise HTTPException(status_code=404, detail="Party not found")
        return party_dto

    async def get_invitation_by_id(self, invitation_id: int, need_exception: bool = False) -> UserPartyDTO | None:
        invitation_dto = await self.repo.get_invitation_by_id(invitation_id)
        if invitation_dto is None and need_exception is True:
            raise HTTPException(status_code=404, detail="Invitation not found")
        return invitation_dto

    async def read_message(self, party_id: int, user_id: int) -> UserPartyDTO | None:
        party_dto = await self.get_party_by_id(party_id, need_exception=True)
        time_now = datetime.now()
        if party_dto.to_user_id == user_id:
            user_party_read_dto = UserPartyReadDTO(
                last_seen_from_user=time_now
            )
        else:
            user_party_read_dto = UserPartyReadDTO(
                last_seen_to_user=time_now
            )

        user_party_dto = await self.repo.read_message(party_id, user_party_read_dto)
        return user_party_dto

    async def accept_invitation(self, invitation_id: int, user_id: int) -> UserInvitationDTO:
        invitation_dto = await self.get_invitation_by_id(invitation_id, need_exception=True)
        status = InvitationStatusEnum.accepted
        if invitation_dto.to_user_id != user_id:
            raise HTTPException(status_code=403, detail="Trying to accept not yours invitation")

        invitation_dto = await self.repo.update_invitation(invitation_id, status)

        party_add_dto = UserPartyAddDTO(
            from_user_id=invitation_dto.from_user_id,
            to_user_id=invitation_dto.to_user_id,
            invitation_id=invitation_id
        )
        party_dto = await self.insert_user_party(party_add_dto)
        return invitation_dto

    async def cancel_invitation(self, invitation_id: int):
        invitation_dto = await self.get_invitation_by_id(invitation_id, need_exception=True)
        status = InvitationStatusEnum.canceled
        invitation_dto = await self.repo.update_invitation(invitation_id, status)
        return invitation_dto

    async def get_user_messages(
            self,
            party_id: int,
            limit: int = 100,
            offset: int = 0,
    ) -> tuple[list[UserMessageDTO], PaginationBaseDTO]:
        user_messages_dto, pagination = await self.repo.get_user_messages(party_id, limit, offset)
        return user_messages_dto, pagination

    async def get_user_parties(
            self,
            user_id: int,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[UserPartyDTO], PaginationBaseDTO]:
        user_party_list_dto, pagination = await self.repo.get_user_parties(user_id, limit, offset)
        return user_party_list_dto, pagination

    async def get_user_invitations(
            self,
            user_id: int,
            mine_sent: bool = False,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[UserInvitationDTO], PaginationBaseDTO]:
        user_invitation_dtos, pagination = await self.repo.get_user_invitations(user_id, mine_sent, limit, offset)

        return user_invitation_dtos, pagination

    async def invitation_exists(self, user_id: int, to_user_id: int):
        user_invitation_dto = await self.repo.get_invitation_by_users(user_id, to_user_id)

        if user_invitation_dto is not None:
            raise HTTPException(status_code=429, detail="Invitation already sent")
