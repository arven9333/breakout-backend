from exceptions.base import AppException


class IconCategoryNotFound(AppException):
    ...


class IconCategoryAlreadyExists(AppException):
    ...


class IconNotFound(AppException):
    ...

class MapLevelAlreadyExists(AppException):
    ...