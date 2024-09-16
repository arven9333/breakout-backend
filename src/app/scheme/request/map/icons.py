from pydantic import BaseModel


class IconCreateScheme(BaseModel):
    category_id: int
    name: str
