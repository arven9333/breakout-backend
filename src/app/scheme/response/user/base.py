from pydantic import BaseModel

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
    stars: str | None = None
    damage: str | None = None
    avatar: UserAvatarScheme | None = None


class UserSearchSchema(UserSchema):
    in_party: bool = False


class UserSearchResponseSchema(BaseModel):
    list: list[UserSearchSchema]
    total: int = 0
    limit: int = 100
    offset: int = 0
