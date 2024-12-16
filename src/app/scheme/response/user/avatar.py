from pydantic import BaseModel


class UserAvatarScheme(BaseModel):
    id: int
    user_id: int
    image: str
    zoom: int = 1
    alignment: int = 1
