from pydantic import BaseModel


class UserGetSchema(BaseModel):
    id: int
    email: str
    username: str
