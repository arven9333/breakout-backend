from pydantic import BaseModel


from scheme.request.common_types import GreatOneInt


class PaginationRequestSchema(BaseModel):
    page: GreatOneInt = 1
    limit: GreatOneInt | int = 100
