from __future__ import annotations
from enums.roles import UserRole
from models.base import BaseModel, Column
from models.common.ts_mixin import TsMixin
from sqlalchemy import BigInteger, String, UniqueConstraint, Boolean, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship


class User(BaseModel, TsMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('email', name='user_items_email_unique'),
        UniqueConstraint('username', name='user_items_username_unique'),
        UniqueConstraint('username_game', name='user_items_username_game_unique'),
        {'extend_existing': True}
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='user id')
    external_id: Mapped[int] = Column(BigInteger, init=False, nullable=True, unique=True)
    username: Mapped[str] = Column(String(127), init=False, nullable=True, comment='username')
    username_game: Mapped[str] = Column(String(127), init=False, nullable=True, comment='username_game')
    bio: Mapped[str] = Column(Text, init=False, nullable=True, comment='bio')

    survival: Mapped[str] = Column(String(255), init=False, nullable=True, comment='survival')
    raids: Mapped[str] = Column(String(255), init=False, nullable=True, comment='raids')
    rank: Mapped[str] = Column(String(127), init=False, nullable=True, comment='rank')
    stars: Mapped[str] = Column(String(255), init=False, nullable=True, comment='stars')
    hours: Mapped[str] = Column(String(255), init=False, nullable=True, comment='hours')
    email: Mapped[str] = Column(String(255), init=False, nullable=True, comment='email')
    password: Mapped[str] = Column(String(255), init=False, nullable=False, comment='password')
    is_active: Mapped[bool] = Column(Boolean, init=False, default=False, nullable=False, comment='deleted')
    role: Mapped[str] = Column(String(127), init=False, server_default=UserRole.default.value)
    find_teammates: Mapped[bool] = Column(Boolean, server_default="false", default=True, nullable=False)

    avatar = relationship('UserAvatar', back_populates="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f"User(id={self.id},username={self.username},email={self.email}"
        )


class UserAvatar(BaseModel, TsMixin):
    __tablename__ = "avatar"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='avatar id')
    user_id: Mapped[int] = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), default=False, nullable=False)
    image: Mapped[str] = Column(String(755), init=False, nullable=True)
    zoom: Mapped[int] = Column(Integer, init=False, nullable=True, server_default="1")
    alignment: Mapped[int] = Column(Integer, init=False, nullable=True, server_default="1")

    user = relationship(User, back_populates="avatar")