from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.clients.database import MasterSessionMakerDep
from repositories.user.user_service import UserServiceRepository


async def get_user_repository(session: MasterSessionMakerDep):
    return UserServiceRepository(
        session=session
    )

USER_REPOSITORY = Annotated[UserServiceRepository, Depends(get_user_repository)]
