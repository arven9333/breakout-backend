from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    premium = "premium"
    default = "default"
