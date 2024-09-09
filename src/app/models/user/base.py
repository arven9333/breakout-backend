from __future__ import annotations

from models.base import BaseModel, Column
from models.common.ts_mixin import TsMixin
from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped


class User(BaseModel, TsMixin):

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('email', name='user_items_email_unique'),
        {"schema": "user"},
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='юзер id')

    first_name: Mapped[str] = Column(String(127), nullable=True,  comment='имя')
    last_name: Mapped[str] = Column(String(127), nullable=True,  comment='фамилия')
    middle_name: Mapped[str] = Column(String(127), nullable=True,  comment='отчество')

    email: Mapped[str] = Column(String(255), nullable=False, comment='email')

    password: Mapped[str] = Column(String(255), nullable=False, comment='password')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f"UserItem(id={self.id},first_name={self.first_name},last_name={self.last_name},"
            f"middle_name={self.middle_name}, emai={self.email}"
        )
