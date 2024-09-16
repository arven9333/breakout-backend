from pydantic import BaseModel


class TokenGetScheme(BaseModel):
    email: str
    password: str
