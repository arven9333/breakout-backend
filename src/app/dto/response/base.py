from dataclasses import dataclass, field
from typing import Optional

from dto.base import DTO


@dataclass
class PaginationBaseDTO(DTO):
    page: int = 1
    limit: Optional[int] = None
    all: Optional[int] = None
    total: Optional[int] = None
    offset: Optional[int] = 0

    def __post_init__(self):
        self.offset = self.limit * (self.page - 1) if self.limit else self.page


@dataclass
class ErrorBaseDto(DTO):
    error_fields: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    success: int = 1
    error: int | None = None
