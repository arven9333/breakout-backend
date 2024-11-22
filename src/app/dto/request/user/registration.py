from dto.base import DTO
from dataclasses import dataclass
from models.user.base import User
from passlib.hash import bcrypt


@dataclass
class UserCreateDTO(DTO):
    username: str
    password: str
    verified_password: str
    email: str | None = None
    external_id: int | None = None

    def get_user_db_create(self):
        return {
            "email": self.email,
            "username": self.username,
            "password": bcrypt.hash(self.password),
            "external_id": self.external_id,
        }


@dataclass
class UserUpdateDTO(DTO):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    external_id: str | None = None


@dataclass
class UserDTO(DTO):
    id: int
    email: str
    username: str
    is_active: bool

    @classmethod
    def from_db_model(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
        )


@dataclass
class UserDBDTO(UserDTO):
    password: str

    @classmethod
    def from_db_model(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            password=user.password
        )
