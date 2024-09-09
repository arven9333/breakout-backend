from typing import Annotated

from fastapi import Depends

from service.user.auth.main import AuthService
from settings import Settings


async def get_auth_service():
    return AuthService(
        jwt_pub_key=Settings.JWT_SECRET_KEY,
        jwt_pri_key=Settings.JWT_SECRET_KEY
    )

AUTH_SERVICE_DEP = Annotated[AuthService, Depends(get_auth_service)]