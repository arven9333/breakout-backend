from dataclasses import dataclass
from dto.base import DTO


@dataclass
class UserDonationAddDTO(DTO):
    name: str | None = None
    total_amount: int | float = 0
    order: int | None = None


@dataclass
class UserDonationUpdateDTO(DTO):
    id: int | None = None
    name: str | None = None
    total_amount: int | float | None = None
    order: int | None = None
