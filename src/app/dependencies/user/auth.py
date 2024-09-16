from typing import Annotated

from fastapi import Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from service.user.auth.main import AuthService
from settings import Settings

AUTHORIZATION_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


async def get_auth_service():
    return AuthService(
        jwt_pub_key=Settings().JWT_SECRET_KEY,
        jwt_pri_key=Settings().JWT_SECRET_KEY
    )


AUTH_SERVICE_DEP = Annotated[AuthService, Depends(get_auth_service)]


async def get_user_id_by_token(
        authorization: str | None = Security(AUTHORIZATION_HEADER)
) -> int:
    service = await get_auth_service()
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    token = service.verify_auth_token(authorization)

    return token.user_id


USER_ID_DEP = Annotated[int, Depends(get_user_id_by_token)]
