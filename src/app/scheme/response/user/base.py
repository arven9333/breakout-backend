from pydantic import BaseModel

from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum
from scheme.response.common import PaginationResponseScheme
from scheme.response.user.avatar import UserAvatarScheme


class UserGetSchema(BaseModel):
    id: int
    email: str | None = None
    username: str


class UserSchema(BaseModel):
    id: int
    is_active: bool
    email: str | None = None
    username: str | None = None
    role: str | None
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool | None = False
    stars: int | None = None
    damage: str | None = None
    avatar: UserAvatarScheme | None = None


class UserInvitationScheme(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    text: str | None
    alias: InvitationTypeEnum
    status: InvitationStatusEnum
    from_user: UserSchema | None = None
    to_user: UserSchema | None = None


class UserInvitationResponseScheme(PaginationResponseScheme):
    list: list[UserInvitationScheme]


class UserSearchSchema(UserSchema):
    invitation: UserInvitationScheme | None = None
    party_id: int | None = None


class UserSearchResponseSchema(BaseModel):
    list: list[UserSearchSchema]
    total: int = 0
    limit: int = 100
    offset: int = 0
