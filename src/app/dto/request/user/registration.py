from dto.base import DTO
from dataclasses import dataclass
from models.user.base import User
from passlib.hash import bcrypt


@dataclass
class UserCreateDTO(DTO):
    email: str
    username: str
    password: str
    verified_password: str

    def get_user_db_create(self):
        return {
            "email": self.email,
            "username": self.username,
            "password": bcrypt.hash(self.password),
        }


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
