from dataclasses import dataclass
from dto.base import DTO


@dataclass
class UserDonationDTO(DTO):
    id: int
    name: str | None = None
    total_amount: int | float = 0
    order: int | None = None
