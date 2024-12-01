from pydantic import BaseModel


class BooleanResponse(BaseModel):
    status: bool
