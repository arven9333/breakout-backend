from pydantic import BaseModel


class BooleanResponse(BaseModel):
    status: bool


class PaginationResponseScheme(BaseModel):
    total: int = 0
    limit: int = 100
    offset: int = 0
