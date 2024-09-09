from typing import Annotated

from dependencies.repo.user_service import USER_REPOSITORY
from fastapi import Depends

from service.user.service.main import UserService


async def get_user_service(user_repository: USER_REPOSITORY):
    return UserService(
        repo=user_repository
    )


USER_SERVICE_DEP = Annotated[UserService, Depends(get_user_service)]