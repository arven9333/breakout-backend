from typing import Annotated

from fastapi import Depends
from dependencies.clients.database import MasterSessionMakerDep
from repositories.user.user_donation import UserDonationRepository


async def get_user_donation_repository(session: MasterSessionMakerDep):
    return UserDonationRepository(
        session=session
    )


USER_DONATION_REPOSITORY = Annotated[UserDonationRepository, Depends(get_user_donation_repository)]
