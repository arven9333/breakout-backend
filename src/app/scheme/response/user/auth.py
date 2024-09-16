from pydantic import BaseModel


class TokenScheme(BaseModel):
    token: str
