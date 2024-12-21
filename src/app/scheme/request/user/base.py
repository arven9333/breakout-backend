from pydantic import BaseModel
from dto.request.user.registration import UserCreateDTO


class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str
    verified_password: str

    def as_dataclass(self):
        return UserCreateDTO(
            **self.model_dump()
        )


class UserUpdateScheme(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    external_id: str | None = None
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool = False
    stars: int | None = None
    damage: str | None = None
