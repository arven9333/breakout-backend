from dto.base import DTO
from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum
from datetime import datetime
from dataclasses import dataclass


@dataclass
class InvitationAddDTO(DTO):
    from_user_id: int
    to_user_id: int
    alias: InvitationTypeEnum
    status: InvitationStatusEnum = InvitationStatusEnum.waiting
    text: str | None = None


@dataclass
class UserPartyAddDTO(DTO):
    from_user_id: int
    to_user_id: int
    invitation_id: int


@dataclass
class UserMessageAddDTO(DTO):
    from_user_id: int
    to_user_id: int
    user_party_id: int
    text: str


@dataclass
class UserPartyReadDTO(DTO):
    last_seen_from_user: datetime | None = None
    last_seen_to_user: datetime | None = None
