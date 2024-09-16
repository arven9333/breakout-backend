from pydantic import BaseModel
from enums.map import MapLevelEnum


class MapScheme(BaseModel):
    id: int
    name: str


class MapLevelScheme(BaseModel):
    id: int
    map_id: int
    level: MapLevelEnum
    leaflet_path: str


class MapLayerScheme(BaseModel):
    id: int
    map_level_id: int
    leaflet_path: str
