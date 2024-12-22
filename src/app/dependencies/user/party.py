from dependencies.repo.party_service import USER_PARTY_REPOSITORY
from service.user.service.party import UserPartyService

from typing import Annotated
from fastapi import Depends


def get_user_party_service(
        user_party_repository: USER_PARTY_REPOSITORY,
) -> UserPartyService:
    return UserPartyService(
        repo=user_party_repository,
    )


USER_PARTY_SERVICE_DEP = Annotated[UserPartyService, Depends(get_user_party_service)]