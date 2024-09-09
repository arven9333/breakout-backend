from dataclasses import dataclass

from dto.base import DTO


@dataclass
class PaginationBaseRequestDTO(DTO):
    page: int = 1
    limit: int = 100

