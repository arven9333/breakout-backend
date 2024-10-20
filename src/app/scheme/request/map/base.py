from pydantic import BaseModel
from enums.map import ModelEnum, ActionEnum


class IconMetricBase(BaseModel):
    coord_x: float
    coord_y: float


class IconMetricBaseCreate(IconMetricBase):
    icon_id: int


class IconMapLevelCreateScheme(IconMetricBaseCreate):
    map_level_id: int


class IconMapLayerCreateScheme(IconMetricBaseCreate):
    map_layer_id: int


class IconMapLayerUpdateScheme(IconMetricBaseCreate):
    icon_layer_id: int


class IconMapLevelUpdateScheme(IconMetricBaseCreate):
    icon_level_id: int


class IconMapLevelDeleteScheme(BaseModel):
    icon_level_id: int


class IconMapLayerDeleteScheme(IconMapLayerUpdateScheme):
    icon_layer_id: int


class ActionScheme(BaseModel):
    action: ActionEnum
    type: ModelEnum
    data: dict
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": "create",
                    "type": "icon_metric_level",
                    "data": {
                        "coord_x": -1.23,
                        "coord_y": 1.23,
                        "icon_id": 1,
                        "map_level_id": 1,
                        "radius": 0.0,
                        "radius_color": "color"
                    }
                },
                {
                    "action": "update",
                    "type": "icon_metric_level",
                    "data": {
                        "icon_level_id": 1,
                        "coord_x": -1.23,
                        "coord_y": 1.23,
                        "icon_id": 1,
                        "map_level_id": 1,
                        "radius": 0.0,
                        "radius_color": "color",
                    }
                },
                {
                    "action": "delete",
                    "type": "icon_metric_level",
                    "data": {
                        "icon_level_id": 1,
                    }
                },
            ]
        }
    }
