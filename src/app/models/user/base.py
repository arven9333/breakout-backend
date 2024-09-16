from __future__ import annotations
from models.base import BaseModel, Column
from models.common.ts_mixin import TsMixin
from sqlalchemy import BigInteger, String, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped


class User(BaseModel, TsMixin):

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('email', name='user_items_email_unique'),
        UniqueConstraint('username', name='user_items_username_unique'),
        {'extend_existing': True}
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False, comment='user id')

    username: Mapped[str] = Column(String(127), init=False, nullable=True,  comment='username')
    email: Mapped[str] = Column(String(255), init=False, nullable=False, comment='email')

    password: Mapped[str] = Column(String(255), init=False, nullable=False, comment='password')
    is_active: Mapped[bool] = Column(Boolean, init=False, default=False, nullable=False, comment='deleted')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f"User(id={self.id},username={self.username},email={self.email}"
        )
