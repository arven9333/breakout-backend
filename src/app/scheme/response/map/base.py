from typing import Optional

from pydantic import BaseModel
from enums.map import MapLevelEnum


class MapScheme(BaseModel):
    id: int
    name: str


class MapLayerScheme(BaseModel):
    id: int
    map_id: int
    leaflet_path: str
    height: Optional[int]
    width: Optional[int]
