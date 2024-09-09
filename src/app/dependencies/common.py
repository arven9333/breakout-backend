from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from settings import Settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_settings():
    settings = Settings()
    return settings


async def get_token(
        authorization: str | None = Security(api_key_header),
):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    return authorization
