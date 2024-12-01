from pydantic import BaseModel


class UserDonationScheme(BaseModel):
    id: int
    name: str | None = None
    order: int | None = None
    total_amount: int | float = 0


class UserDonationListResponseScheme(BaseModel):
    user_donations: list[UserDonationScheme]
