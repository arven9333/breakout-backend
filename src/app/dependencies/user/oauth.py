from typing import Annotated
from fastapi import Depends

from dependencies.user.auth import AUTH_SERVICE_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from service.user.auth.oauth import OauthService


def get_oauth_service(
        auth_service: AUTH_SERVICE_DEP,
        user_service: USER_SERVICE_DEP,
) -> OauthService:
    return OauthService(
        auth_service=auth_service,
        user_service=user_service
    )


OAUTH_SERVICE_DEP = Annotated[OauthService, Depends(get_oauth_service)]
