from dataclasses import dataclass

from dto.request.user.donation import UserDonationAddDTO, UserDonationUpdateDTO
from dto.response.user.donation import UserDonationDTO

from repositories.user.user_donation import UserDonationRepository


@dataclass
class UserDonationService:
    repo: UserDonationRepository

    async def add_user_donation(self, user_donation_add_dto: UserDonationAddDTO) -> UserDonationDTO:
        user_donation_dto = await self.repo.add_user_donation(user_donation_add_dto)
        return user_donation_dto

    async def update_user_donation(
            self,
            user_donation_update_dtos: list[UserDonationUpdateDTO]
    ) -> list[UserDonationDTO]:
        result = []
        for user_donation_update_dto in user_donation_update_dtos:
            user_donation_id = user_donation_update_dto.id
            user_donation_update_dto.id = None

            user_donation_dto = await self.repo.update_user_donation(
                user_donation_update_dto=user_donation_update_dto,
                user_donation_id=user_donation_id,
            )
            result.append(user_donation_dto)

        return result

    async def get_user_donations_list(self) -> list[UserDonationDTO]:
        user_donation_dtos = await self.repo.get_user_donations_list()
        return user_donation_dtos
