from pydantic import BaseModel


class TokenGetScheme(BaseModel):
    subject: str
    password: str

