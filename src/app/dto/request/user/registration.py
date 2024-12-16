from dto.base import DTO
from dataclasses import dataclass

from models.user.base import User
from passlib.hash import bcrypt


class AvatarDTO(DTO):
    id: int
    user_id: int
    image: str
    zoom: str
    alignment: str


@dataclass
class UserCreateDTO(DTO):
    username: str
    password: str
    verified_password: str
    email: str | None = None
    external_id: int | None = None
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool = False

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
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool = False


@dataclass
class UserDTO(DTO):
    id: int
    email: str
    username: str
    is_active: bool
    role: str | None
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool = False
    avatar: AvatarDTO | None = None

    @classmethod
    def from_db_model(cls, user: User, **kwargs):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            role=user.role,
            raids=user.raids,
            rank=user.rank,
            survival=user.survival,
            hours=user.hours,
            bio=user.hours,
            username_game=user.username_game,
            find_teammates=user.find_teammates,
        )


@dataclass
class UserDBDTO(DTO):
    password: str
    id: int
    email: str
    username: str
    is_active: bool
    role: str | None
    survival: str | None = None
    raids: str | None = None
    rank: str | None = None
    hours: str | None = None
    bio: str | None = None
    username_game: str | None = None
    find_teammates: bool = False
    avatar: AvatarDTO | None = None

    @classmethod
    def from_db_model(cls, user: User, **kwargs):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            password=user.password,
            role=user.role,
            raids=user.raids,
            rank=user.rank,
            survival=user.survival,
            hours=user.hours,
            bio=user.hours,
            username_game=user.username_game,
            find_teammates=user.find_teammates,
        )
