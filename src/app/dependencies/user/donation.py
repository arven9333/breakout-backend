from dependencies.repo.donation_service import USER_DONATION_REPOSITORY
from service.user.service.donation import UserDonationService

from typing import Annotated
from fastapi import Depends


def get_user_donation_service(
        user_donation_repository: USER_DONATION_REPOSITORY,
) -> UserDonationService:
    return UserDonationService(
        repo=user_donation_repository,
    )


USER_DONATION_SERVICE_DEP = Annotated[UserDonationService, Depends(get_user_donation_service)]
