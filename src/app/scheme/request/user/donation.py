from pydantic import BaseModel
from dto.request.user.donation import UserDonationAddDTO, UserDonationUpdateDTO


class UserDonationAddScheme(BaseModel):
    name: str | None = None
    order: int | None = None
    total_amount: int | float = 0

    def as_dataclass(self):
        return UserDonationAddDTO(
            name=self.name,
            order=self.order,
            total_amount=self.total_amount,
        )


class UserDonationUpdateScheme(BaseModel):
    id: int
    name: str | None = None
    order: int | None = None
    total_amount: int | float = 0

    def as_dataclass(self):
        return UserDonationUpdateDTO(
            id=self.id,
            name=self.name,
            order=self.order,
            total_amount=self.total_amount,
        )
