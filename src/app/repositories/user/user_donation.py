from sqlalchemy import (
    select,
    insert,
    update
)

import logging
from _logging.base import setup_logging

from repositories.base import SQLAlchemyRepo
from dto.request.user.donation import UserDonationAddDTO, UserDonationUpdateDTO
from dto.response.user.donation import UserDonationDTO
from models.user.donation import UserDonation

logger = logging.getLogger(__name__)
setup_logging(__name__)


class UserDonationRepository(SQLAlchemyRepo):
    async def add_user_donation(self, user_donation_add_dto: UserDonationAddDTO) -> UserDonationDTO:
        query = insert(
            UserDonation
        ).values(
            **user_donation_add_dto.as_dict()
        ).returning(
            UserDonation
        )

        async with self.session as session:
            result = await session.execute(query)
            if user_donation := result.scalar_one():
                user_donation_dto = UserDonationDTO.model_to_dto(user_donation)
        return user_donation_dto

    async def update_user_donation(
            self,
            user_donation_update_dto: UserDonationUpdateDTO,
            user_donation_id: int | None,
    ) -> UserDonationDTO:

        query = update(
            UserDonation
        ).values(
            **user_donation_update_dto.as_dict(exclude_none=True)
        ).where(
            UserDonation.id == user_donation_id,
        ).returning(
            UserDonation
        )

        async with self.session as session:
            result = await session.execute(query)
            if user_donation := result.scalar_one():
                user_donation_dto = UserDonationDTO.model_to_dto(user_donation)
        return user_donation_dto

    async def get_user_donations_list(self) -> list[UserDonationDTO]:
        query = select(
            UserDonation
        ).order_by(
            UserDonation.order
        )
        result_donations = []

        async with self.session as session:
            result = await session.execute(query)
            if user_donations := result.scalars().all():
                for user_donation in user_donations:
                    user_donation_dto = UserDonationDTO.model_to_dto(user_donation)
                    result_donations.append(user_donation_dto)

        return result_donations
