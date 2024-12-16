from pydantic import BaseModel


class UserAvatarCreateScheme(BaseModel):
    zoom: int = 1
    alignment: int = 1


class UserAvatarUpdateScheme(BaseModel):
    zoom: int | None = None
    alignment: int | None = None
