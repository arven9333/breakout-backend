from pydantic import BaseModel
from enums.map import MapLevelEnum


class MapScheme(BaseModel):
    id: int
    name: str


class MapLayerScheme(BaseModel):
    id: int
    map_id: int
    leaflet_path: str
