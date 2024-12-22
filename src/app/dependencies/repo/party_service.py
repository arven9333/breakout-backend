from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.user.user_party import UserPartyRepository


async def get_user_party_repository(session: MasterSessionMakerDep):
    return UserPartyRepository(
        session=session
    )

USER_PARTY_REPOSITORY = Annotated[UserPartyRepository, Depends(get_user_party_repository)]
