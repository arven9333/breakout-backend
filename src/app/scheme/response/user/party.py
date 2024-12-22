from scheme.response.user.base import UserSchema
from scheme.response.common import BooleanResponse, PaginationResponseScheme
from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum

from datetime import datetime
from pydantic import BaseModel


class UserInvitationScheme(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    text: str | None
    alias: InvitationTypeEnum
    status: InvitationStatusEnum
    from_user: UserSchema | None = None
    to_user: UserSchema | None = None


class UserMessageScheme(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    user_party_id: int
    text: str
    from_user: UserSchema | None = None
    to_user: UserSchema | None = None
    ts_create: datetime = None


class LastUserMessageScheme(UserMessageScheme):
    is_read: bool = False


class UserPartyScheme(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    invitation_id: int
    last_seen_to_user: datetime | None = None
    last_seen_from_user: datetime | None = None
    from_user: UserSchema | None = None
    to_user: UserSchema | None = None
    last_message: LastUserMessageScheme | None = None


class UserInvitationResponseScheme(PaginationResponseScheme):
    list: list[UserInvitationScheme]


class UserPartyResponseScheme(PaginationResponseScheme):
    list: list[UserPartyScheme]


class UserMessageResponseScheme(PaginationResponseScheme):
    list: list[UserMessageScheme]
