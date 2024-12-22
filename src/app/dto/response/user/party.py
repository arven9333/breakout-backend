from dto.base import DTO
from dto.response.user.base import UserDTO
from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum

from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserInvitationDTO(DTO):
    id: int
    from_user_id: int
    to_user_id: int
    text: str | None
    alias: InvitationTypeEnum
    status: InvitationStatusEnum
    from_user: UserDTO | None = None
    to_user: UserDTO | None = None


@dataclass
class UserMessageDTO(DTO):
    id: int
    from_user_id: int
    to_user_id: int
    user_party_id: int
    text: str
    from_user: UserDTO | None = None
    to_user: UserDTO | None = None
    ts_create: datetime | None = None


@dataclass
class LastUserMessageDTO(UserMessageDTO):
    is_read: bool = False


@dataclass
class UserPartyDTO(DTO):
    id: int
    from_user_id: int
    to_user_id: int
    invitation_id: int
    last_seen_to_user: datetime | None = None
    last_seen_from_user: datetime | None = None
    from_user: UserDTO | None = None
    to_user: UserDTO | None = None
    last_message: LastUserMessageDTO | None = None


@dataclass
class UserInvitationGroupDTO(DTO):
    got: list[UserInvitationDTO]
    sent: list[UserInvitationDTO]
