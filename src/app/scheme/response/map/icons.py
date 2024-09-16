from pydantic import BaseModel


class IconScheme(BaseModel):
    id: int
    image: str
    category_id: int
    name: str


class IconCategoryScheme(BaseModel):
    id: int
    name: str

