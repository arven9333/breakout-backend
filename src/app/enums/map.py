from enum import Enum


class ActionEnum(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"



class ModelEnum(str, Enum):
    icon_metric_level = "icon_metric_level"
    icon_metric_figure = "icon_metric_figure"


class MapLevelEnum(str, Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'


class MapStatusEnum(str, Enum):
    public = "public"
    wait = "wait"
    hide = "hide"
