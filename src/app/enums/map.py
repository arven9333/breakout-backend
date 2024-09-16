from enum import Enum


class ActionEnum(Enum):
    create = "create"
    update = "update"
    delete = "delete"


class ModelEnum(Enum):
    icon_metric_layer = "icon_metric_layer"
    icon_metric_level = "icon_metric_level"


class MapLevelEnum(Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'
